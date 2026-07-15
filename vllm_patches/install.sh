#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-python}"

if [[ -d "$TARGET" ]]; then
  PYTHON_BIN="$TARGET/bin/python"
else
  PYTHON_BIN="$TARGET"
fi

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "ERROR: Python interpreter is not executable: $PYTHON_BIN" >&2
  exit 1
fi

VLLM_VERSION="$($PYTHON_BIN -c 'import vllm; print(vllm.__version__)')"
APPLY_CONTEXT_CUTOFF="${AIMO_VLLM_APPLY_DFLASH_CONTEXT_CUTOFF:-1}"
if [[ "$APPLY_CONTEXT_CUTOFF" == "1" && "$VLLM_VERSION" == "0.25.1" ]]; then
  "$PYTHON_BIN" "$ROOT/patch_dflash_context_cutoff.py" "$PYTHON_BIN"
elif [[ "$APPLY_CONTEXT_CUTOFF" == "1" ]]; then
  echo "[vllm-patch] skipping V1 DFlash context cutoff for vLLM $VLLM_VERSION"
fi

BUILD_ROOT="$(mktemp -d)"
trap 'rm -rf "$BUILD_ROOT"' EXIT
cp "$ROOT/pyproject.toml" "$ROOT/README.md" "$BUILD_ROOT/"
cp -R "$ROOT/src" "$BUILD_ROOT/src"

"$PYTHON_BIN" -m pip install \
  --no-deps \
  --no-build-isolation \
  --disable-pip-version-check \
  "$BUILD_ROOT"

VLLM_PLUGINS=olmo3_sink "$PYTHON_BIN" - <<'PY'
import os

from vllm import ModelRegistry
from vllm.config.speculative import SpeculativeConfig
from vllm.plugins import load_general_plugins

if (
    __import__("vllm").__version__ == "0.25.1"
    and os.environ.get("AIMO_VLLM_APPLY_DFLASH_CONTEXT_CUTOFF", "1") == "1"
):
    from types import SimpleNamespace

    from vllm.v1.core.sched.scheduler import (
        _batch_reaches_speculation_context_cutoff,
    )

    if "disable_above_context_len" not in SpeculativeConfig.__dataclass_fields__:
        raise RuntimeError("DFlash context cutoff field was not installed")
    requests = {"req": SimpleNamespace(num_computed_tokens=81918)}
    assert not _batch_reaches_speculation_context_cutoff(
        requests,
        {"req": 1},
        81920,
    )
    assert _batch_reaches_speculation_context_cutoff(
        requests,
        {"req": 2},
        81920,
    )

load_general_plugins()
expected_architectures = {
    "Olmo3SinkForCausalLM": "Olmo3SinkForCausalLM",
}
if __import__("vllm").__version__ == "0.25.1":
    expected_architectures.update(
        {
            "Olmo3SinkDFlashForCausalLM": "Olmo3SinkDFlashForCausalLM",
            "DFlashDraftModel": "Olmo3SinkDFlashForCausalLM",
        }
    )

for architecture, expected_class_name in expected_architectures.items():
    if architecture not in ModelRegistry.get_supported_archs():
        raise RuntimeError(f"vLLM plugin did not register {architecture}")
    model_class = ModelRegistry._try_load_model_cls(architecture)
    if model_class is None or model_class.__name__ != expected_class_name:
        raise RuntimeError(
            f"vLLM resolved {architecture} to {model_class}, expected "
            f"{expected_class_name}"
        )
    print(f"[vllm-patch] registered {architecture} -> "
          f"{model_class.__module__}:{model_class.__name__}")
PY
