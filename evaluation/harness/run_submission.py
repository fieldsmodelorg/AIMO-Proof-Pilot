"""Run proof search for test.csv and write id,proof rows to submission.csv."""

from __future__ import annotations

import argparse
import asyncio
import csv
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from async_client import AsyncChatClient
from eval_config import active_model, load_config
from proof_search import ProblemSearch
from trace_uploader import (
    TraceUploader,
    load_hf_token,
    resolve_run_name,
    traces_config,
)


EXPECTED_COLUMNS = ["id", "problem"]
OUTPUT_COLUMNS = ["id", "proof"]


@dataclass(frozen=True)
class InputRow:
    id: str
    problem: str


def select_problems(
    rows: list["InputRow"], problems: str = "all", limit: int = 0
) -> list["InputRow"]:
    """Pick which problems to run (benchmark/dev convenience).

    ``problems`` selects a subset by the test.csv ``id`` column:
      - "all" (default): every row, in CSV order.
      - a comma-separated id list, e.g. "1,4,5": those problems, in the order
        requested. Nothing is hardcoded -- any subset the input defines is valid.
    ``limit`` > 0 then keeps only the first ``limit`` of the selected rows (the
    "number of problems" knob). The two compose, e.g. problems="1,4,5", limit=2
    -> ids 1,4.

    Unknown ids fail fast. The result is never empty.
    """
    spec = (problems or "all").strip()
    if spec in ("", "all"):
        selected = list(rows)
    else:
        wanted = [token.strip() for token in spec.split(",") if token.strip()]
        # de-duplicate while preserving requested order
        seen: set[str] = set()
        wanted = [w for w in wanted if not (w in seen or seen.add(w))]
        by_id = {row.id: row for row in rows}
        missing = [w for w in wanted if w not in by_id]
        if missing:
            raise ValueError(
                f"--problems requested id(s) {missing} not in input; "
                f"available ids: {[row.id for row in rows]}"
            )
        selected = [by_id[w] for w in wanted]
    if limit > 0:
        selected = selected[:limit]
    if not selected:
        raise ValueError("problem selection is empty (check --problems/--limit)")
    return selected


def load_test_csv(path: Path) -> list[InputRow]:
    with path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                "test.csv must contain exactly these columns in order: id,problem"
            )
        rows = []
        seen_ids: set[str] = set()
        for line_number, source_row in enumerate(reader, start=2):
            if None in source_row:
                raise ValueError(
                    "test.csv must contain exactly two fields on "
                    f"line {line_number}"
                )
            row_id = source_row["id"]
            problem = source_row["problem"]
            if row_id is None or not row_id.strip():
                raise ValueError(f"test.csv line {line_number} has an empty id")
            if row_id != row_id.strip():
                raise ValueError(
                    f"test.csv line {line_number} id has surrounding whitespace"
                )
            if row_id in seen_ids:
                raise ValueError(f"test.csv contains duplicate id {row_id!r}")
            if problem is None or not problem.strip():
                raise ValueError(
                    f"test.csv line {line_number} has an empty problem"
                )
            seen_ids.add(row_id)
            rows.append(InputRow(id=row_id, problem=problem))
    if not rows:
        raise ValueError("test.csv must contain at least one problem")
    return rows


def pin_file(source: Path, destination: Path) -> None:
    if destination.exists():
        if source.read_bytes() != destination.read_bytes():
            raise RuntimeError(
                f"submission resume input differs from pinned file: {destination}"
            )
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def load_existing_submission(path: Path, rows: list[InputRow]) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != OUTPUT_COLUMNS:
            raise RuntimeError(
                "existing submission.csv must contain exactly id,proof"
            )
        proofs = []
        for index, output_row in enumerate(reader):
            if index >= len(rows) or None in output_row:
                raise RuntimeError("existing submission.csv is not an input prefix")
            if output_row["id"] != rows[index].id:
                raise RuntimeError("existing submission.csv IDs are not an input prefix")
            proof = output_row["proof"]
            if proof is None or not proof.strip():
                raise RuntimeError("existing submission.csv contains an empty proof")
            replace_proof(proofs, index, proof)
    return proofs


def replace_proof(proofs: list[str], index: int, proof: str) -> None:
    if index > len(proofs):
        raise RuntimeError("cannot checkpoint a non-prefix submission row")
    if index == len(proofs):
        proofs.append(proof)
    else:
        proofs[index] = proof

def write_submission(
    path: Path,
    rows: list[InputRow],
    proofs: list[str],
) -> None:
    if len(proofs) > len(rows):
        raise ValueError("proof count cannot exceed input row count")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row, proof in zip(rows, proofs, strict=False):
            writer.writerow({"id": row.id, "proof": proof})
    os.replace(temporary, path)


async def run_submission(
    config_path: Path,
    input_path: Path,
    output_path: Path,
    artifacts_dir: Path,
    problems: str = "all",
    limit: int = 0,
) -> None:
    config_path = config_path.resolve()
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    artifacts_dir = artifacts_dir.resolve()
    rows = load_test_csv(input_path)
    rows = select_problems(rows, problems=problems, limit=limit)
    if problems != "all" or limit > 0:
        print(
            "[submission] problem selection: problems={} limit={} -> {} problem(s) "
            "ids={}".format(problems, limit, len(rows), [row.id for row in rows]),
            flush=True,
        )
    config = load_config(config_path)
    model = active_model(config)

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    pinned_input = artifacts_dir / "test.csv"
    pinned_config = artifacts_dir / "config.yaml"
    is_resume = pinned_input.exists() and pinned_config.exists()
    pin_file(input_path, pinned_input)
    pin_file(config_path, pinned_config)

    server = config["server"]
    client = AsyncChatClient(
        f"http://{server['host']}:{server['port']}/v1",
        str(model.target),
        api_key="EMPTY",
        max_connections=config["search"]["concurrency"] + 8,
        timeout=float(config["search"]["request_timeout_seconds"]),
    )
    semaphore = asyncio.Semaphore(config["search"]["concurrency"])
    proofs = load_existing_submission(output_path, rows) if is_resume else []
    if not is_resume:
        write_submission(output_path, rows, proofs)

    # Optional: periodically push the whole artifacts tree (reasoning traces) to a
    # HF dataset. Init fails fast (bad token / missing secrets), but once running,
    # individual upload errors are swallowed so they can't kill the proof run.
    traces = traces_config(config)
    stop_uploads: asyncio.Event | None = None
    upload_task: asyncio.Task | None = None
    if traces is not None:
        # Resolve the HF token. A configured secrets_file is explicit intent, so a
        # missing/invalid one still fails fast. With no secrets_file we use the
        # ambient token (HF_TOKEN env or `hf auth login`); if there is NONE, skip
        # uploads with a warning rather than crashing the run -- no token just
        # means "don't upload".
        secrets_file = traces["secrets_file"].strip()
        if secrets_file:
            token = load_hf_token(secrets_file)
        else:
            from huggingface_hub import get_token

            token = get_token()
        if token is None:
            print(
                "[traces] enabled but no HF token found (HF_TOKEN unset and no "
                "`hf auth login`); skipping trace upload",
                flush=True,
            )
            traces = None
    if traces is not None:
        run_name = resolve_run_name(traces["run_name"], model.target)
        uploader = TraceUploader(
            artifacts_dir=artifacts_dir,
            dataset_repo=traces["dataset_repo"],
            token=token,
            run_name=run_name,
            private=traces["private"],
            interval_seconds=traces["interval_seconds"],
            output_path=output_path,  # mirror submission.csv into the upload
        )
        uploader.ensure_repo()
        stop_uploads = asyncio.Event()
        upload_task = asyncio.create_task(uploader.run_periodic(stop_uploads))
        print(
            f"[traces] uploading artifacts to {uploader.repo}:{run_name} "
            f"every {traces['interval_seconds']}s",
            flush=True,
        )

    try:
        for index, row in enumerate(rows):
            internal_id = f"row-{index:04d}"
            async def checkpoint(
                value: dict,
                *,
                current_index: int = index,
                current_row: InputRow = row,
            ) -> None:
                proof = value["proof"]
                if not isinstance(proof, str) or not proof.strip():
                    raise RuntimeError("round checkpoint contains an empty proof")
                replace_proof(proofs, current_index, proof)
                write_submission(output_path, rows, proofs)
                print(
                    "[submission] id={} round={} selected={}".format(
                        current_row.id,
                        value["round"],
                        value["selected_proof_id"],
                    ),
                    flush=True,
                )

            search = ProblemSearch(
                problem_id=internal_id,
                problem=row.problem,
                output_dir=artifacts_dir / "problems" / internal_id,
                client=client,
                semaphore=semaphore,
                config=config["search"],
                on_round_complete=checkpoint,
            )
            result = await search.solve()
            proof = result["final_proof"]
            if not isinstance(proof, str) or not proof.strip():
                raise RuntimeError(
                    f"proof search returned an empty proof for id {row.id!r}"
                )
            replace_proof(proofs, index, proof)
            write_submission(output_path, rows, proofs)
            print(
                f"[submission] id={row.id} rows={index + 1}/{len(rows)} "
                f"selected={result['selected_proof_id']}",
                flush=True,
            )
    finally:
        # Stop periodic uploads and do one final flush so the last rounds land,
        # even if the search raised.
        if upload_task is not None:
            assert stop_uploads is not None
            stop_uploads.set()
            try:
                await upload_task
            except Exception as error:  # a broken final upload must not mask the run's result
                print(f"[traces] final upload error: {error!r}", flush=True)
        await client.aclose()
    print(f"[submission] complete -> {output_path}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input", default=Path("test.csv"), type=Path)
    parser.add_argument("--output", default=Path("submission.csv"), type=Path)
    parser.add_argument(
        "--artifacts-dir", default=Path("submission_artifacts"), type=Path
    )
    parser.add_argument(
        "--problems",
        default="all",
        help=(
            "Which problems to run, selected by test.csv id: 'all' (default) or "
            "a comma-separated id list like '1,4,5' (run in the order given)."
        ),
    )
    parser.add_argument(
        "--limit",
        default=0,
        type=int,
        help=(
            "Cap the run to the first N selected problems (0 = no cap). "
            "Composes with --problems; this is the 'number of problems' knob."
        ),
    )
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit must be >= 0")
    asyncio.run(
        run_submission(
            args.config,
            args.input,
            args.output,
            args.artifacts_dir,
            problems=args.problems,
            limit=args.limit,
        )
    )

if __name__ == "__main__":
    main()
