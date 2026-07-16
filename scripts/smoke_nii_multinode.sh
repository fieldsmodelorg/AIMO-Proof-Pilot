#!/usr/bin/env bash
set -euo pipefail

VLLM_VERSION="${VLLM_VERSION:-0.25.1}"
RUNTIME_ROOT="${NII_INFERENCE_RUNTIME_ROOT:-/tmp/aimo-proof-pilot-inference-runtime}"
REPO_DIR="${NII_INFERENCE_REPO_DIR:-$RUNTIME_ROOT/repo}"
VENV="${NII_INFERENCE_VENV:-$RUNTIME_ROOT/venv-vllm-$VLLM_VERSION}"
RANK="${AIMO_NODE_RANK:-${GLOBAL_RANK:-${NODE_RANK:-0}}}"
WORLD_SIZE="${WORLD_SIZE:-8}"
RUN_ID="${NII_SMOKE_RUN_ID:?set one shared NII_SMOKE_RUN_ID on every node}"
SMOKE_ROOT="${NII_SMOKE_ROOT:-$RUNTIME_ROOT/smoke/$RUN_ID}"
MASTER_PORT="${NII_SMOKE_MASTER_PORT:-29671}"
WAIT_SECONDS="${NII_SMOKE_WAIT_SECONDS:-300}"
MASTER_FILE="$SMOKE_ROOT/master_addr"

wait_for_file() {
  local path="$1"
  local deadline=$((SECONDS + WAIT_SECONDS))
  while [[ ! -f "$path" ]]; do
    if (( SECONDS >= deadline )); then
      echo "ERROR: timed out waiting for $path" >&2
      return 1
    fi
    sleep 1
  done
}

mkdir -p "$SMOKE_ROOT"
if [[ "$RANK" == "0" ]]; then
  address="${NII_SMOKE_MASTER_ADDR:-}"
  if [[ -z "$address" ]]; then
    address="$(hostname -I | awk '{print $1}')"
  fi
  test -n "$address"
  printf '%s\n' "$address" > "$MASTER_FILE.tmp"
  mv "$MASTER_FILE.tmp" "$MASTER_FILE"
fi
wait_for_file "$MASTER_FILE"

export GLOBAL_RANK="$RANK"
export WORLD_SIZE
export MASTER_ADDR="$(cat "$MASTER_FILE")"
export MASTER_PORT
export AIMO_DISTRIBUTED_ROOT="$SMOKE_ROOT/distributed"
export AIMO_DISTRIBUTED_RUN_ID="$RUN_ID"
export AIMO_DISTRIBUTED_TIMEOUT_SECONDS="$WAIT_SECONDS"
export AIMO_DISTRIBUTED_POLL_SECONDS=0.2
export NII_INFERENCE_REPO_COMMIT="$(git -C "$REPO_DIR" rev-parse HEAD)"
export VLLM_PLUGINS=olmo3_sink
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"
unset RANK LOCAL_RANK LOCAL_WORLD_SIZE

"$VENV/bin/python" "$REPO_DIR/scripts/nii_multinode_smoke.py"
