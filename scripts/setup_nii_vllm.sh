#!/usr/bin/env bash
set -euo pipefail

VLLM_VERSION="${VLLM_VERSION:-0.25.1}"
REPO_URL="${NII_INFERENCE_REPO_URL:-https://github.com/nguyen599/aimo-proof-pilot-inference.git}"
REPO_REF="${NII_INFERENCE_REPO_REF:-main}"
RUNTIME_ROOT="${NII_INFERENCE_RUNTIME_ROOT:-/tmp/aimo-proof-pilot-inference-runtime}"
REPO_DIR="${NII_INFERENCE_REPO_DIR:-$RUNTIME_ROOT/repo}"
VENV="${NII_INFERENCE_VENV:-$RUNTIME_ROOT/venv-vllm-$VLLM_VERSION}"
MODEL_ROOT="${NII_MODEL_ROOT:-/tmp/models}"
TARGET_REPO="${NII_TARGET_MODEL_REPO:-nguyen599/olmo3-opd-sft-425}"
TARGET_NAME="${NII_TARGET_MODEL_NAME:-olmo3-opd-sft-425}"
TARGET_DIR="${NII_TARGET_MODEL_DIR:-$MODEL_ROOT/$TARGET_NAME}"
TARGET_VIEW="${NII_TARGET_MODEL_VIEW:-$MODEL_ROOT/$TARGET_NAME-vllm}"
DFLASH_DIR="${NII_DFLASH_MODEL_DIR:-$MODEL_ROOT/dflash-32b-draft-v2test-phaseL}"
DOWNLOAD_MODEL="${NII_DOWNLOAD_TARGET_MODEL:-1}"
WAIT_SECONDS="${NII_SETUP_WAIT_SECONDS:-7200}"
RANK="${AIMO_NODE_RANK:-${GLOBAL_RANK:-${NODE_RANK:-0}}}"
SCRIPT_HASH="$(sha256sum "${BASH_SOURCE[0]}" | awk '{print substr($1, 1, 12)}')"

log() {
  printf '[nii-vllm-setup] rank=%s host=%s %s\n' "$RANK" "$(hostname)" "$*"
}

wait_for_file() {
  local path="$1"
  local description="$2"
  local deadline=$((SECONDS + WAIT_SECONDS))
  while [[ ! -f "$path" ]]; do
    if (( SECONDS >= deadline )); then
      echo "ERROR: timed out waiting for $description: $path" >&2
      return 1
    fi
    sleep 2
  done
}

clone_or_update_repo() {
  mkdir -p "$RUNTIME_ROOT"
  if [[ -d "$REPO_DIR/.git" ]]; then
    git -C "$REPO_DIR" fetch --depth 1 origin "$REPO_REF"
    git -C "$REPO_DIR" checkout -B runtime FETCH_HEAD
    git -C "$REPO_DIR" reset --hard FETCH_HEAD
    return
  fi

  local temporary="$REPO_DIR.tmp.$$"
  rm -rf "$temporary"
  git clone --depth 1 --branch "$REPO_REF" "$REPO_URL" "$temporary"
  rm -rf "$REPO_DIR"
  mv "$temporary" "$REPO_DIR"
}

install_runtime() {
  log "creating shared venv at $VENV"
  if [[ ! -x "$VENV/bin/python" ]]; then
    rm -rf "$VENV"
    uv venv --python /usr/bin/python3 --system-site-packages --seed "$VENV"
  fi

  uv pip install --python "$VENV/bin/python" --no-deps \
    "vllm==$VLLM_VERSION" \
    "nest-asyncio>=1.6,<2"

  bash "$REPO_DIR/vllm_patches/install.sh" "$VENV"

  NII_EXPECTED_VENV="$VENV" \
  VLLM_PLUGINS=olmo3_sink \
  "$VENV/bin/python" - <<'PY'
import importlib.util
import os
from pathlib import Path

import vllm
from vllm import ModelRegistry
from vllm.plugins import load_general_plugins

expected = Path(os.environ["NII_EXPECTED_VENV"]).resolve()
loaded = Path(vllm.__file__).resolve()
if vllm.__version__ != "0.25.1":
    raise RuntimeError(f"Expected vLLM 0.25.1, got {vllm.__version__}")
if expected not in loaded.parents:
    raise RuntimeError(f"vLLM was loaded outside the NII venv: {loaded}")
for module in ("pandas", "pyarrow", "openai", "nest_asyncio", "torch"):
    if importlib.util.find_spec(module) is None:
        raise RuntimeError(f"Required module is unavailable: {module}")
load_general_plugins()
for architecture in (
    "Olmo3SinkForCausalLM",
    "Olmo3SinkDFlashForCausalLM",
    "DFlashDraftModel",
):
    if architecture not in ModelRegistry.get_supported_archs():
        raise RuntimeError(f"Plugin architecture is unavailable: {architecture}")
print(f"[nii-vllm-setup] import smoke passed: {vllm.__version__} {loaded}")
PY
}

download_target_model() {
  if [[ "$DOWNLOAD_MODEL" != "1" ]]; then
    log "target download disabled"
    return
  fi
  if [[ -f "$TARGET_DIR/model.safetensors.index.json" ]]; then
    log "target checkpoint already present at $TARGET_DIR"
  else
    local hf_cli
    hf_cli="$(command -v hf || true)"
    if [[ -z "$hf_cli" ]]; then
      echo "ERROR: Hugging Face CLI 'hf' is unavailable" >&2
      return 1
    fi
    mkdir -p "$TARGET_DIR"
    log "downloading $TARGET_REPO to $TARGET_DIR"
    HF_XET_HIGH_PERFORMANCE=0 "$hf_cli" download "$TARGET_REPO" \
      --local-dir "$TARGET_DIR"
  fi

  "$VENV/bin/python" - "$TARGET_DIR" <<'PY'
import json
import sys
from pathlib import Path

from safetensors import safe_open

root = Path(sys.argv[1])
index_path = root / "model.safetensors.index.json"
config_path = root / "config.json"
if not index_path.is_file() or not config_path.is_file():
    raise RuntimeError(f"Incomplete model directory: {root}")
index = json.loads(index_path.read_text())
shards = sorted(set(index["weight_map"].values()))
if not shards:
    raise RuntimeError("Model index references no shards")
for shard_name in shards:
    shard = root / shard_name
    if not shard.is_file() or shard.stat().st_size == 0:
        raise RuntimeError(f"Missing or empty shard: {shard}")
    with safe_open(shard, framework="pt", device="cpu") as source:
        if not source.keys():
            raise RuntimeError(f"Shard has no tensors: {shard}")
print(f"[nii-vllm-setup] validated model shards={len(shards)} root={root}")
PY

  "$VENV/bin/python" "$REPO_DIR/scripts/prepare_vllm_model_view.py" \
    "$TARGET_DIR" "$TARGET_VIEW"
}

mkdir -p "$RUNTIME_ROOT/markers" "$MODEL_ROOT"
REPO_READY="$RUNTIME_ROOT/markers/repo-$SCRIPT_HASH.ready"
SETUP_READY="$RUNTIME_ROOT/markers/setup-$SCRIPT_HASH-vllm-$VLLM_VERSION-$TARGET_NAME.ready"

if [[ "$RANK" == "0" ]]; then
  exec 9>"$RUNTIME_ROOT/setup.lock"
  flock 9
  rm -f "$REPO_READY" "$SETUP_READY"
  clone_or_update_repo
  git -C "$REPO_DIR" rev-parse HEAD > "$REPO_READY"
  install_runtime
  download_target_model
  test -f "$DFLASH_DIR/config.json" || {
    echo "ERROR: DFlash checkpoint is missing: $DFLASH_DIR/config.json" >&2
    exit 1
  }
  {
    echo "repo_commit=$(git -C "$REPO_DIR" rev-parse HEAD)"
    echo "vllm_version=$VLLM_VERSION"
    echo "venv=$VENV"
    echo "target_model=$TARGET_DIR"
    echo "target_view=$TARGET_VIEW"
    echo "dflash_model=$DFLASH_DIR"
  } > "$SETUP_READY"
  log "setup complete: $SETUP_READY"
else
  wait_for_file "$REPO_READY" "rank-0 repository checkout"
  wait_for_file "$SETUP_READY" "rank-0 vLLM setup"
fi

export VLLM_PLUGINS=olmo3_sink
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"
"$VENV/bin/python" -c \
  'import vllm, run; assert vllm.__version__ == "0.25.1"; print("node import ok", vllm.__version__)'
cat "$SETUP_READY"
