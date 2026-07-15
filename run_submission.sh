#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VENV:-/workspace/pp/venv}"
PYTHON="${PYTHON:-$VENV/bin/python}"
INPUT="${1:-test.csv}"
OUTPUT="${2:-submission.csv}"
CONFIG="${CONFIG:?CONFIG is required and must point to config.yaml}"
ARTIFACTS_DIR="${ARTIFACTS_DIR:-submission_artifacts}"

if [[ ! -x "$PYTHON" ]]; then
  printf 'Python interpreter is not executable: %s\n' "$PYTHON" >&2
  exit 1
fi

exec "$PYTHON" "$REPO/evaluation/harness/run_submission.py" \
  --config "$CONFIG" \
  --input "$INPUT" \
  --output "$OUTPUT" \
  --artifacts-dir "$ARTIFACTS_DIR"
