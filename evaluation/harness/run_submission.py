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


EXPECTED_COLUMNS = ["id", "problem"]
OUTPUT_COLUMNS = ["id", "proof"]


@dataclass(frozen=True)
class InputRow:
    id: str
    problem: str


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
) -> None:
    config_path = config_path.resolve()
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    artifacts_dir = artifacts_dir.resolve()
    rows = load_test_csv(input_path)
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
    args = parser.parse_args()
    asyncio.run(
        run_submission(
            args.config,
            args.input,
            args.output,
            args.artifacts_dir,
        )
    )

if __name__ == "__main__":
    main()
