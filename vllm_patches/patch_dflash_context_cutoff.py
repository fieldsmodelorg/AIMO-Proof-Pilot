#!/usr/bin/env python3
"""Add a batch-wide context cutoff to vLLM 0.25.1's V1 drafter.

The scheduler sets the next draft width to zero at the cutoff, including when
async scheduling is enabled. The V1 worker then skips the drafter while keeping
vLLM's native K-wide zero buffer for async bookkeeping, so the target model
continues ordinary one-token decoding without stale or missing draft storage.

The patch is source-shaped, idempotent, and fail-closed. It deliberately does
not patch Model Runner V2 because this repository forces
``VLLM_USE_V2_MODEL_RUNNER=0``.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path


SUPPORTED_VERSION = "0.25.1"
BACKUP_SUFFIX = ".pre_dflash_context_cutoff"

CONFIG_PATH = Path("config/speculative.py")
SCHEDULER_PATH = Path("v1/core/sched/scheduler.py")
RUNNER_PATH = Path("v1/worker/gpu_model_runner.py")

CONFIG_MARKER = "DFLASH_CONTEXT_CUTOFF_CONFIG"
SCHEDULER_HELPER_MARKER = "DFLASH_CONTEXT_CUTOFF_BATCH_DECISION"
SCHEDULER_GATE_MARKER = "DFLASH_CONTEXT_CUTOFF_SCHEDULER_GATE"
RUNNER_GATE_MARKER = "DFLASH_CONTEXT_CUTOFF_V1_GATE"

CONFIG_ORIGINAL = '''    max_model_len: int | None = Field(default=None, ge=1)
    """The maximum model length of the draft model. Used when testing the
    ability to skip speculation for some sequences."""
'''

CONFIG_PATCHED = (
    CONFIG_ORIGINAL
    + '''    # DFLASH_CONTEXT_CUTOFF_CONFIG
    disable_above_context_len: int | None = Field(default=None, ge=1)
    """Disable draft proposals when the largest scheduled sequence in the
    current batch has reached this context length. The target model continues
    normal decoding. This currently applies to the V1 model runner."""
'''
)

SCHEDULER_HELPER_INSERTION = "logger = init_logger(__name__)\n"

SCHEDULER_HELPER_PATCHED = '''logger = init_logger(__name__)


# DFLASH_CONTEXT_CUTOFF_BATCH_DECISION
def _batch_reaches_speculation_context_cutoff(
    requests: dict[str, Request],
    num_scheduled_tokens: dict[str, int],
    cutoff: int | None,
) -> bool:
    """Return whether the V1 batch should stop producing new draft tokens."""
    if cutoff is None or not num_scheduled_tokens:
        return False
    max_scheduled_seq_len = max(
        requests[req_id].num_computed_tokens + num_tokens
        for req_id, num_tokens in num_scheduled_tokens.items()
    )
    return max_scheduled_seq_len >= cutoff
'''

SCHEDULER_INIT_ORIGINAL = """        self.dynamic_sd_lookup: list[int] | None = None
        if speculative_config is not None:
"""

SCHEDULER_INIT_PATCHED = """        self.dynamic_sd_lookup: list[int] | None = None
        self.disable_speculation_above_context_len = (
            speculative_config.disable_above_context_len
            if speculative_config is not None
            else None
        )
        if speculative_config is not None:
"""

SCHEDULER_DECISION_ORIGINAL = """        # Dynamic speculative decoding: compute optimal K
        num_spec_tokens_to_schedule = self.num_spec_tokens
        if self.dynamic_sd_lookup is not None and len(num_scheduled_tokens) > 0:
            num_spec_tokens_to_schedule = self.dynamic_sd_lookup[
                len(num_scheduled_tokens)
            ]
"""

SCHEDULER_DECISION_PATCHED = (
    SCHEDULER_DECISION_ORIGINAL
    + """
        # DFLASH_CONTEXT_CUTOFF_SCHEDULER_GATE: setting K=0 keeps the V1
        # async scheduler's placeholders and the worker's proposal width in
        # agreement. Model Runner V2 is intentionally unchanged.
        if not self.use_v2_model_runner and _batch_reaches_speculation_context_cutoff(
            self.requests,
            num_scheduled_tokens,
            self.disable_speculation_above_context_len,
        ):
            num_spec_tokens_to_schedule = 0
"""
)

RUNNER_GATE_ORIGINAL = """            input_fits_in_drafter = self._input_fits_in_drafter(
                spec_decode_common_attn_metadata
            )
"""

RUNNER_GATE_PATCHED = """            # DFLASH_CONTEXT_CUTOFF_V1_GATE: the scheduler uses a
            # zero proposal width at the context cutoff. Honor that decision
            # before launching any draft-model work.
            input_fits_in_drafter = (
                scheduler_output.num_spec_tokens_to_schedule > 0
                and self._input_fits_in_drafter(
                    spec_decode_common_attn_metadata
                )
            )
"""

EMPTY_DRAFTS_ORIGINAL = """            if not input_fits_in_drafter:
                # Zero out draft tokens so the scheduler doesn't schedule
                # stale drafts from the previous step.
                # For Nemotron-H: it is necessary to zero out the draft tokens,
                # otherwise the stale tokens will corrupt Mamba recurrent
                # state and logprobs for sequences near max_model_len.
                self._draft_token_ids = torch.zeros(
                    1, device=self.device, dtype=torch.int32
                ).expand(len(self.input_batch.req_ids), self.num_spec_tokens)
                self._draft_probs = None
                self._draft_prob_req_ids = None
                self._copy_draft_token_ids_to_cpu(scheduler_output, zeros_only=True)
"""

LEGACY_EMPTY_DRAFTS_PATCHED = """            if not input_fits_in_drafter:
                # DFLASH_CONTEXT_CUTOFF_EMPTY_DRAFTS: publish an explicit
                # zero-width draft for every request. Empty lists clear stale
                # scheduler state and make the next step target-only; token id 0
                # is a real token and must not be used as a no-draft sentinel.
                self._draft_token_ids = torch.empty(
                    (len(self.input_batch.req_ids), 0),
                    device=self.device,
                    dtype=torch.int32,
                )
                self._draft_probs = None
                self._draft_prob_req_ids = None
                self._copy_draft_token_ids_to_cpu(scheduler_output, zeros_only=True)
"""


def _replace_once(source: str, original: str, patched: str, label: str) -> str:
    if patched in source:
        return source
    count = source.count(original)
    if count != 1:
        raise RuntimeError(f"Expected exactly one {label} patch point, found {count}")
    return source.replace(original, patched, 1)


def patch_config_source(source: str) -> str:
    source = _replace_once(
        source,
        CONFIG_ORIGINAL,
        CONFIG_PATCHED,
        "SpeculativeConfig context cutoff",
    )
    if source.count(CONFIG_MARKER) != 1:
        raise RuntimeError("SpeculativeConfig context cutoff marker is incomplete")
    return source


def patch_scheduler_source(source: str) -> str:
    source = _replace_once(
        source,
        SCHEDULER_HELPER_INSERTION,
        SCHEDULER_HELPER_PATCHED,
        "scheduler context-cutoff helper",
    )
    source = _replace_once(
        source,
        SCHEDULER_INIT_ORIGINAL,
        SCHEDULER_INIT_PATCHED,
        "scheduler context-cutoff configuration",
    )
    source = _replace_once(
        source,
        SCHEDULER_DECISION_ORIGINAL,
        SCHEDULER_DECISION_PATCHED,
        "scheduler context-cutoff decision",
    )
    if source.count(SCHEDULER_HELPER_MARKER) != 1:
        raise RuntimeError("Scheduler cutoff helper marker is incomplete")
    if source.count(SCHEDULER_GATE_MARKER) != 1:
        raise RuntimeError("Scheduler cutoff gate marker is incomplete")
    return source


def patch_runner_source(source: str) -> str:
    # Migrate the first cutoff implementation. A zero-width tensor is unsafe
    # with async scheduling: the following scheduler iteration may still carry
    # K invalid draft placeholders and _prepare_input_ids must have a K-wide
    # source tensor available while it discards them.
    if LEGACY_EMPTY_DRAFTS_PATCHED in source:
        source = source.replace(
            LEGACY_EMPTY_DRAFTS_PATCHED,
            EMPTY_DRAFTS_ORIGINAL,
            1,
        )
    source = _replace_once(
        source,
        RUNNER_GATE_ORIGINAL,
        RUNNER_GATE_PATCHED,
        "V1 zero-width proposal gate",
    )
    if source.count(RUNNER_GATE_MARKER) != 1:
        raise RuntimeError("V1 context cutoff marker is incomplete")
    if "DFLASH_CONTEXT_CUTOFF_EMPTY_DRAFTS" in source:
        raise RuntimeError("Legacy zero-width DFlash draft patch remains installed")
    return source


def _installed_vllm(interpreter: Path) -> tuple[Path, str]:
    script = (
        "import pathlib, vllm; "
        "print(pathlib.Path(vllm.__file__).resolve().parent); "
        "print(vllm.__version__)"
    )
    result = subprocess.run(
        [str(interpreter), "-c", script],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = result.stdout.strip().splitlines()
    if len(lines) != 2:
        raise RuntimeError(f"Could not locate vLLM with {interpreter}: {result.stdout}")
    return Path(lines[0]), lines[1]


def _version_from_root(root: Path) -> str | None:
    version_path = root / "_version.py"
    if not version_path.is_file():
        return None
    match = re.search(
        r"^__version__ = version = ['\"]([^'\"]+)",
        version_path.read_text(),
        re.M,
    )
    return match.group(1) if match else None


def resolve_vllm_root(target: Path) -> tuple[Path, str | None]:
    # Keep a venv's bin/python path intact. Resolving that symlink can turn it
    # into the base interpreter and silently import vLLM from the system prefix.
    target = target.expanduser().absolute()
    if (target / CONFIG_PATH).is_file():
        return target, _version_from_root(target)
    if target.is_dir():
        target = target / "bin/python"
    if not target.is_file():
        raise RuntimeError(
            f"Expected a vLLM root, venv, or Python executable: {target}"
        )
    return _installed_vllm(target)


def _write_patched(path: Path, patcher) -> None:
    original = path.read_text()
    patched = patcher(original)
    compile(patched, str(path), "exec")
    if patched == original:
        print(f"  verified: {path}")
        return
    backup = path.with_name(path.name + BACKUP_SUFFIX)
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(patched)
    print(f"  patched: {path}")
    pycache = path.parent / "__pycache__"
    if pycache.is_dir():
        for cached in pycache.glob(f"{path.stem}.*.pyc"):
            cached.unlink()


def patch_vllm(root: Path) -> None:
    paths = (root / CONFIG_PATH, root / SCHEDULER_PATH, root / RUNNER_PATH)
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"Missing expected vLLM source files: {missing}")
    _write_patched(paths[0], patch_config_source)
    _write_patched(paths[1], patch_scheduler_source)
    _write_patched(paths[2], patch_runner_source)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <vllm_root|venv|python>")
    root, version = resolve_vllm_root(Path(sys.argv[1]))
    if version is not None and version != SUPPORTED_VERSION:
        raise RuntimeError(
            f"This patch targets vLLM {SUPPORTED_VERSION}, found {version} at {root}"
        )
    print(f"[vllm-patch] source={root} version={version or 'source-tree'}")
    patch_vllm(root)
    print("[vllm-patch] V1 DFlash context cutoff verified")


if __name__ == "__main__":
    main()
