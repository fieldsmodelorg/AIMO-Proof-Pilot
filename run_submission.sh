#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV="${VENV:-/workspace/pp/venv}"
PYTHON="${PYTHON:-$VENV/bin/python}"
# Default input = the committed IMO-2026 set (exact 6-problem CSV validated on NII).
INPUT="${1:-$REPO/evaluation/data/imo2026-latex-test.csv}"
OUTPUT="${2:-submission.csv}"
CONFIG="${CONFIG:?CONFIG is required and must point to config.yaml}"
ARTIFACTS_DIR="${ARTIFACTS_DIR:-submission_artifacts}"
# Problem selection (benchmark/dev convenience). PROBLEMS: 'all' (default) or an
# id list like '1,4,5' (run in order). LIMIT: first-N cap (0=off). Both optional.
PROBLEMS="${PROBLEMS:-all}"
LIMIT="${LIMIT:-0}"

if [[ ! -x "$PYTHON" ]]; then
  printf 'Python interpreter is not executable: %s\n' "$PYTHON" >&2
  exit 1
fi

exec "$PYTHON" "$REPO/evaluation/harness/run_submission.py" \
  --config "$CONFIG" \
  --input "$INPUT" \
  --output "$OUTPUT" \
  --artifacts-dir "$ARTIFACTS_DIR" \
  --problems "$PROBLEMS" \
  --limit "$LIMIT"
