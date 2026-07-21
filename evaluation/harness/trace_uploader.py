"""Periodic upload of proof-search artifacts (reasoning traces) to a HF dataset.

The proof search writes a complete trace under the run's artifacts dir:
`problems/<id>/calls.jsonl` (every model call, with `reasoning_content` and
`content`), plus `prompts/`, `proofs/`, `rounds/` and `final.json`. This module
snapshots that whole tree to a HuggingFace dataset on a fixed interval and once
more at shutdown, so a long run's traces are durably captured as it goes.

Uploads go through `upload_large_folder`, which splits a big tree into many
commits and is resumable -- a single all-at-once `upload_folder` commit stalls
(HTTP 413 / "large folder" rejection) once a run's `calls.jsonl` grows to
hundreds of MB. `upload_large_folder` has no `path_in_repo`, so we hardlink-
mirror the artifacts under a per-run staging dir (`<run_out>/.hf_stage/<run_name>/`)
and upload that, keeping each run namespaced. The judge-facing `submission.csv`
(written OUTSIDE the artifacts dir, atomically rewritten each round -> a folder
mirror of it goes stale) is uploaded explicitly with `upload_file`, which always
commits current content.

Auth comes from a secrets file (JSON or YAML) that is NOT the config and never
leaves the node -- the config only stores its path. Upload failures are logged
and swallowed: a flaky network must never kill a multi-hour proof run.
"""
from __future__ import annotations

import asyncio
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml

# Never ship these into the dataset even if they land under the artifacts dir.
IGNORE_PATTERNS = [
    "*.tmp", "**/*.tmp",
    "SECRETS.*", "**/SECRETS.*",
    "*.token", "**/*.token",
    ".git", ".git/**",
]

# Extra excludes for the bulk (large-folder) upload: submission.csv is uploaded
# explicitly (see `_upload_submission`) so the atomically-rewritten file never
# goes stale, and upload_large_folder's own metadata dir must never be shipped.
LARGE_FOLDER_IGNORE = IGNORE_PATTERNS + [
    "submission.csv", "**/submission.csv",
    ".cache/**", "**/.cache/**",
]

_TOKEN_KEYS = ("hf_token", "huggingface_token", "HF_TOKEN", "token")


def load_hf_token(secrets_file: str) -> str:
    """Read the HF token from a JSON/YAML secrets file (yaml.safe_load reads both)."""
    path = Path(secrets_file).expanduser()
    if not path.is_file():
        raise FileNotFoundError(
            f"traces.secrets_file not found: {path} -- create it with an "
            '"hf_token" entry, e.g. {"hf_token": "hf_..."}'
        )
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON/YAML object")
    for key in _TOKEN_KEYS:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValueError(
        f"{path} has no token; expected one of {list(_TOKEN_KEYS)}"
    )


def resolve_run_name(run_name: str, target: Path) -> str:
    """Subfolder in the dataset for this run. Empty -> the target model's name,
    so each checkpoint (e.g. opd-32b-bf16-step-225) gets its own namespace."""
    name = run_name.strip().strip("/")
    return name or Path(target).name


def stage_output_file(output_path: Path | None, artifacts_dir: Path) -> None:
    """Copy the submission CSV into the artifacts dir (standalone helper).

    The submission is written to a separate --output path, outside the artifacts
    dir. `TraceUploader` no longer relies on this mirror -- it uploads the real
    submission.csv explicitly (see `TraceUploader._upload_submission`) so the
    atomically-rewritten file never goes stale. Retained for callers that want a
    local copy alongside the artifacts. No-op if unset or not yet written; never raises.
    """
    if output_path is None:
        return
    src = Path(output_path)
    if not src.is_file():
        return
    try:
        shutil.copy2(src, Path(artifacts_dir) / src.name)
    except OSError as error:
        print(f"[traces] could not stage {src.name}: {error}", flush=True)


class TraceUploader:
    def __init__(
        self,
        *,
        artifacts_dir: Path,
        dataset_repo: str,
        token: str | None,
        run_name: str,
        private: bool,
        interval_seconds: int,
        output_path: Path | None = None,
    ) -> None:
        # Lazy import: huggingface_hub is only needed when traces are enabled, so
        # the rest of the harness (and its tests) never require it.
        from huggingface_hub import HfApi

        self.api = HfApi(token=token)
        self.artifacts_dir = Path(artifacts_dir)
        self.repo = dataset_repo.strip().strip("/")
        self.run_name = run_name
        self.private = private
        self.interval = interval_seconds
        # Submission CSV, written outside artifacts_dir; uploaded explicitly on
        # each cycle (see _upload_submission) rather than mirrored into the tree.
        self.output_path = Path(output_path) if output_path is not None else None
        # Hardlink staging so upload_large_folder (which has no path_in_repo) can
        # namespace the run under <run_name>/. Kept beside artifacts_dir so it is
        # on the same filesystem (hardlinks require it) and cleaned up with the run.
        self._stage_root = self.artifacts_dir.parent / ".hf_stage"
        self._stage_run = self._stage_root / self.run_name
        self._count = 0

    def ensure_repo(self) -> None:
        """Create the dataset if missing (a no-op if it already exists). Does not
        change an existing repo's visibility."""
        self.api.create_repo(
            self.repo, repo_type="dataset", private=self.private, exist_ok=True
        )

    def _refresh_stage(self) -> None:
        """Hardlink-mirror the artifacts tree into <stage>/<run_name>/.

        Hardlinks are cheap and reflect appended files (e.g. calls.jsonl) in place;
        --remove-destination re-links any file rewritten via atomic replace so the
        staged copy always matches. submission.csv is never staged -- it is uploaded
        explicitly from its real path so a stale folder mirror can't shadow it.
        """
        self._stage_run.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["cp", "-al", "--remove-destination",
             f"{self.artifacts_dir}/.", f"{self._stage_run}/"],
            stderr=subprocess.PIPE, text=True, check=False,
        )
        if result.returncode != 0:
            print(
                f"[traces] staging hardlink warning: {result.stderr.strip()[:200]}",
                flush=True,
            )
        try:
            (self._stage_run / "submission.csv").unlink()
        except FileNotFoundError:
            pass

    def _upload_submission(self, label: str) -> None:
        """Upload the real submission.csv straight to <run_name>/submission.csv.

        upload_file always commits the current bytes, so this small file (rewritten
        atomically each round -> a new inode) never lags behind the run, unlike a
        folder mirror that upload_large_folder may skip as "unchanged"."""
        if self.output_path is None or not self.output_path.is_file():
            return
        try:
            self.api.upload_file(
                path_or_fileobj=str(self.output_path),
                path_in_repo=f"{self.run_name}/submission.csv",
                repo_id=self.repo,
                repo_type="dataset",
                commit_message=f"traces: {label} submission #{self._count}",
            )
        except Exception as error:  # best-effort, like the bulk upload
            print(f"[traces] submission upload failed (continuing): {error!r}", flush=True)

    def upload_once(self, label: str) -> bool:
        self._count += 1
        # Small, judge-facing file first so it is current even if the bulk is slow.
        self._upload_submission(label)
        self._refresh_stage()
        try:
            self.api.upload_large_folder(
                repo_id=self.repo,
                repo_type="dataset",
                folder_path=str(self._stage_root),
                ignore_patterns=LARGE_FOLDER_IGNORE,
                print_report=False,
            )
            return True
        except Exception as error:  # never let an upload kill the run
            print(f"[traces] upload failed (continuing): {error!r}", flush=True)
            return False

    async def run_periodic(self, stop: asyncio.Event) -> None:
        """Upload every `interval` seconds until `stop` is set, then a final flush.

        Uploads run in a worker thread so the async search loop keeps serving; only
        one upload is ever in flight (the loop awaits each before scheduling the next).
        """
        while True:
            stopped = False
            try:
                await asyncio.wait_for(stop.wait(), timeout=self.interval)
                stopped = True
            except asyncio.TimeoutError:
                pass
            await asyncio.to_thread(
                self.upload_once, "final" if stopped else "periodic"
            )
            if stopped:
                return


def traces_config(config: dict[str, Any]) -> dict[str, Any] | None:
    """The traces section iff uploads are enabled, else None."""
    traces = config.get("traces")
    if isinstance(traces, dict) and traces.get("enabled"):
        return traces
    return None
