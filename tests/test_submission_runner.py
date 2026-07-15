import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

import run_submission as submission_runner
from run_submission import InputRow, load_test_csv, write_submission


class SubmissionCsvTests(unittest.TestCase):
    def test_accepts_user_supplied_ids_zero_through_five(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "test.csv"
            path.write_text(
                "id,problem\n"
                + "".join(
                    f"{index},Problem {index}\n" for index in range(6)
                ),
                encoding="utf-8",
            )
            rows = load_test_csv(path)
        self.assertEqual([row.id for row in rows], [str(index) for index in range(6)])

    def test_round_trip_preserves_ids_order_and_multiline_proofs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "test.csv"
            input_path.write_text(
                'id,problem\n0,"Prove A."\n1,"Prove B."\n', encoding="utf-8"
            )
            rows = load_test_csv(input_path)
            self.assertEqual(
                rows,
                [InputRow("0", "Prove A."), InputRow("1", "Prove B.")],
            )

            output_path = root / "submission.csv"
            write_submission(output_path, rows, ["First\nproof", "Second proof"])
            with output_path.open(newline="", encoding="utf-8") as source:
                reader = csv.DictReader(source)
                self.assertEqual(reader.fieldnames, ["id", "proof"])
                self.assertEqual(
                    list(reader),
                    [
                        {"id": "0", "proof": "First\nproof"},
                        {"id": "1", "proof": "Second proof"},
                    ],
                )

    def test_requires_exact_lowercase_columns(self):
        for content in (
            'ID,problem\n0,"Prove A."\n',
            'id,Problem\n0,"Prove A."\n',
            'id,problem,answer\n0,"Prove A.",ignored\n',
            'id,problem\n0,"Prove A.",ignored\n',
        ):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "test.csv"
                path.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "exactly"):
                    load_test_csv(path)

    def test_rejects_empty_and_duplicate_ids(self):
        cases = (
            ('id,problem\n,"Prove A."\n', "empty id"),
            ('id,problem\n0,"Prove A."\n0,"Prove B."\n', "duplicate id"),
        )
        for content, message in cases:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "test.csv"
                path.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, message):
                    load_test_csv(path)

    def test_partial_output_contains_only_completed_rows(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "submission.csv"
            rows = [InputRow("0", "A"), InputRow("1", "B")]
            write_submission(path, rows, ["proof A"])
            with path.open(newline="", encoding="utf-8") as source:
                self.assertEqual(
                    list(csv.DictReader(source)),
                    [{"id": "0", "proof": "proof A"}],
                )


class SubmissionRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_failed_search_keeps_latest_round_checkpoint(self):
        class FakeClient:
            def __init__(self, *args, **kwargs):
                pass

            async def aclose(self):
                pass

        class FailingSearch:
            def __init__(self, **kwargs):
                self.on_round_complete = kwargs["on_round_complete"]

            async def solve(self):
                await self.on_round_complete(
                    {
                        "round": 1,
                        "proof": "Round 1 recoverable proof",
                        "selected_proof_id": "r01-p0001",
                    }
                )
                raise RuntimeError("simulated failure before round 2")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "test.csv"
            output_path = root / "submission.csv"
            input_path.write_text(
                "id,problem\n0,Prove the claim.\n", encoding="utf-8"
            )
            with (
                patch.object(submission_runner, "AsyncChatClient", FakeClient),
                patch.object(submission_runner, "ProblemSearch", FailingSearch),
                self.assertRaisesRegex(RuntimeError, "simulated failure"),
            ):
                await submission_runner.run_submission(
                    REPO / "config.yaml",
                    input_path,
                    output_path,
                    root / "artifacts",
                )

            with output_path.open(newline="", encoding="utf-8") as source:
                self.assertEqual(
                    list(csv.DictReader(source)),
                    [{"id": "0", "proof": "Round 1 recoverable proof"}],
                )

    async def test_runner_checkpoints_each_round_and_writes_exact_schema(self):
        seen: list[tuple[str, str]] = []
        writes: list[list[str]] = []
        original_write = submission_runner.write_submission

        def track_write(path, rows, proofs):
            writes.append(list(proofs))
            original_write(path, rows, proofs)

        class FakeClient:
            def __init__(self, *args, **kwargs):
                pass

            async def aclose(self):
                pass

        class FakeSearch:
            def __init__(self, *, problem_id, problem, **kwargs):
                seen.append((problem_id, problem))
                self.problem_id = problem_id
                self.on_round_complete = kwargs["on_round_complete"]

            async def solve(self):
                for round_index in (1, 2):
                    await self.on_round_complete(
                        {
                            "round": round_index,
                            "proof": (
                                f"Round {round_index} proof for {self.problem_id}"
                            ),
                            "selected_proof_id": (
                                f"{self.problem_id}-round-{round_index}"
                            ),
                        }
                    )
                return {
                    "final_proof": f"Proof for {self.problem_id}",
                    "selected_proof_id": f"{self.problem_id}-selected",
                }

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "test.csv"
            output_path = root / "submission.csv"
            input_path.write_text(
                "id,problem\na,\"Only statement A\"\nb,\"Only statement B\"\n",
                encoding="utf-8",
            )
            with (
                patch.object(submission_runner, "AsyncChatClient", FakeClient),
                patch.object(submission_runner, "ProblemSearch", FakeSearch),
                patch.object(
                    submission_runner,
                    "write_submission",
                    side_effect=track_write,
                ),
            ):
                await submission_runner.run_submission(
                    REPO / "config.yaml",
                    input_path,
                    output_path,
                    root / "artifacts",
                )

            self.assertEqual(
                writes,
                [
                    [],
                    ["Round 1 proof for row-0000"],
                    ["Round 2 proof for row-0000"],
                    ["Proof for row-0000"],
                    ["Proof for row-0000", "Round 1 proof for row-0001"],
                    ["Proof for row-0000", "Round 2 proof for row-0001"],
                    ["Proof for row-0000", "Proof for row-0001"],
                ],
            )
            self.assertEqual(
                seen,
                [("row-0000", "Only statement A"), ("row-0001", "Only statement B")],
            )
            with output_path.open(newline="", encoding="utf-8") as source:
                self.assertEqual(
                    list(csv.DictReader(source)),
                    [
                        {"id": "a", "proof": "Proof for row-0000"},
                        {"id": "b", "proof": "Proof for row-0001"},
                    ],
                )

            writes.clear()
            with (
                patch.object(submission_runner, "AsyncChatClient", FakeClient),
                patch.object(submission_runner, "ProblemSearch", FakeSearch),
                patch.object(
                    submission_runner,
                    "write_submission",
                    side_effect=track_write,
                ),
            ):
                await submission_runner.run_submission(
                    REPO / "config.yaml",
                    input_path,
                    output_path,
                    root / "artifacts",
                )
            self.assertEqual(
                writes[0],
                ["Round 1 proof for row-0000", "Proof for row-0001"],
            )


if __name__ == "__main__":
    unittest.main()
