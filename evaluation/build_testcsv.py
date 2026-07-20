"""Build a solver test.csv (id,problem) from a HuggingFace dataset.

Extracts ONLY the id and problem columns and writes the exact schema
run_submission expects. Any other column (reference_solution, grading_scheme,
points, answer, ...) is deliberately DROPPED and reported -- the solver runs in
contestant regime and must never see judge-side material.

Usage:
    python evaluation/build_testcsv.py --dataset bogoconic1/IMO-2026-Problems -o test.csv
    python evaluation/build_testcsv.py --dataset chankhavu/IMO2026-GPT-5.6-Sol-Markscheme \
        --token "$HF_TOKEN" -o test.csv     # private dataset
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.request

ID_COLS = ("id", "problem_idx", "index", "idx")
PROBLEM_COLS = ("problem", "problem_statement", "statement", "question")
# Anything resembling judge-side material -- never emitted, loudly flagged.
JUDGE_COLS = ("reference_solution", "solution", "grading_scheme", "markscheme",
              "points", "answer", "answer_key", "rubric")


def _fetch(dataset, config, split, token, offset, length):
    url = (f"https://datasets-server.huggingface.co/rows?dataset={dataset}"
           f"&config={config}&split={split}&offset={offset}&length={length}")
    req = urllib.request.Request(url, headers={"User-Agent": "build-testcsv/1"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def _pick(cols, candidates, kind):
    for c in candidates:
        if c in cols:
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--config", default="default")
    ap.add_argument("--split", default="train")
    ap.add_argument("-o", "--output", default="test.csv")
    ap.add_argument("--token", default=os.environ.get("HF_TOKEN"))
    ap.add_argument("--id-col", help="override id column")
    ap.add_argument("--problem-col", help="override problem column")
    args = ap.parse_args()

    first = _fetch(args.dataset, args.config, args.split, args.token, 0, 100)
    total = first.get("num_rows_total", 0)
    cols = [f["name"] for f in first.get("features", [])]
    id_col = args.id_col or _pick(cols, ID_COLS, "id")
    prob_col = args.problem_col or _pick(cols, PROBLEM_COLS, "problem")
    if prob_col is None:
        print(f"ERROR: no problem column in {cols}; use --problem-col", file=sys.stderr)
        return 2
    dropped = [c for c in cols if c not in (id_col, prob_col)]
    judge = [c for c in dropped if c in JUDGE_COLS]

    rows, offset = [], 0
    while offset < total:
        page = first if offset == 0 else _fetch(
            args.dataset, args.config, args.split, args.token, offset, 100)
        batch = page.get("rows", [])
        if not batch:
            break
        for r in batch:
            row = r["row"]
            rid = str(row[id_col]) if id_col else str(r["row_idx"])
            # datasets-server silently truncates large cells; refuse to emit one
            # so the output is guaranteed byte-exact with the source dataset.
            if prob_col in (r.get("truncated_cells") or []):
                print(
                    f"ERROR: problem at id {rid} was truncated by datasets-server; "
                    "the output would not be bit-exact. Build from the dataset file "
                    "directly instead.",
                    file=sys.stderr,
                )
                return 2
            problem = row[prob_col]
            if not isinstance(problem, str) or not problem.strip():
                print(f"ERROR: empty problem at id {rid}", file=sys.stderr)
                return 2
            rows.append((rid.strip(), problem))
        offset += len(batch)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "problem"])
        w.writerows(rows)

    print(f"wrote {len(rows)} problems -> {args.output}")
    print(f"  id column     : {id_col or '(row index)'}")
    print(f"  problem column: {prob_col}")
    if dropped:
        print(f"  DROPPED columns (not given to solver): {dropped}")
    if judge:
        print(f"  ^ includes judge-side material kept OUT of the solver: {judge}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
