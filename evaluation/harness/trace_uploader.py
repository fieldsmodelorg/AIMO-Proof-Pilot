"""Periodic upload of proof-search artifacts (reasoning traces) to a HF dataset.

The proof search writes a complete trace under the run's artifacts dir:
`problems/<id>/calls.jsonl` (every model call, with `reasoning_content` and
`content`), plus `prompts/`, `proofs/`, `rounds/` and `final.json`. This module
snapshots that whole tree to a HuggingFace dataset on a fixed interval and once
more at shutdown, so a long run's traces are durably captured as it goes.

Auth comes from a secrets file (JSON or YAML) that is NOT the config and never
leaves the node -- the config only stores its path. Upload failures are logged
and swallowed: a flaky network must never kill a multi-hour proof run.
"""
from __future__ import annotations

import asyncio
import shutil
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
    """Copy the submission CSV into the artifacts dir so it uploads with the tree.

    The submission is written to a separate --output path, outside the uploaded
    artifacts dir; mirroring the latest copy in lets teammates grab all final
    answers from one file on HF. No-op if unset or not yet written; never raises.
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
        # Submission CSV (written outside artifacts_dir); mirrored in on each
        # upload so it rides along to HF.
        self.output_path = output_path
        self._count = 0

    def ensure_repo(self) -> None:
        """Create the dataset if missing (a no-op if it already exists). Does not
        change an existing repo's visibility."""
        self.api.create_repo(
            self.repo, repo_type="dataset", private=self.private, exist_ok=True
        )

    def upload_once(self, label: str) -> bool:
        self._count += 1
        stage_output_file(self.output_path, self.artifacts_dir)
        try:
            self.api.upload_folder(
                folder_path=str(self.artifacts_dir),
                repo_id=self.repo,
                repo_type="dataset",
                path_in_repo=self.run_name,
                commit_message=f"traces: {label} snapshot #{self._count}",
                ignore_patterns=IGNORE_PATTERNS,
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
