from __future__ import annotations

import csv
import json
import os
import socket
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from evaluation.harness_vllm import run  # noqa: E402


def free_tcp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class DistributedRuntimeTests(unittest.TestCase):
    def test_detects_global_rank_and_assigns_global_candidates(self):
        with patch.dict(
            os.environ,
            {
                "GLOBAL_RANK": "3",
                "WORLD_SIZE": "8",
                "MASTER_ADDR": "10.0.0.1",
                "MASTER_PORT": "29500",
            },
            clear=True,
        ):
            distributed = run.DistributedRuntime.from_environment()

        self.assertEqual(distributed.rank, 3)
        self.assertEqual(distributed.world_size, 8)
        self.assertEqual(distributed.assigned_attempt_indices(14), [3, 11])
        self.assertEqual(
            [distributed.assigned_attempt_indices(14, rank=rank) for rank in range(8)],
            [
                [0, 8],
                [1, 9],
                [2, 10],
                [3, 11],
                [4, 12],
                [5, 13],
                [6],
                [7],
            ],
        )

    def test_merge_restores_global_candidate_order(self):
        payloads = []
        for rank in range(2):
            assigned = list(range(rank, 4, 2))
            payloads.append(
                {
                    "rank": rank,
                    "assigned_attempts": assigned,
                    "pipeline_result": {
                        "candidates": [
                            {
                                "attempt_idx": attempt_idx,
                                "proof_solution": f"proof-{attempt_idx}",
                                "strict_pass": attempt_idx == 3,
                            }
                            for attempt_idx in reversed(assigned)
                        ],
                        "failed_attempts": [],
                        "skipped_generations": [],
                        "cancelled_count": rank,
                    },
                }
            )

        merged = run.merge_distributed_pipeline_results(
            payloads,
            pipelines_per_problem=4,
            world_size=2,
        )

        self.assertEqual(
            [candidate["attempt_idx"] for candidate in merged["candidates"]],
            [0, 1, 2, 3],
        )
        self.assertEqual(merged["strict_pass_candidate"]["attempt_idx"], 3)
        self.assertEqual(merged["cancelled_count"], 1)

    def test_merge_accepts_ranks_without_assigned_candidates(self):
        payloads = [
            {
                "rank": rank,
                "assigned_attempts": [rank] if rank < 2 else [],
                "pipeline_result": {
                    "candidates": (
                        [{"attempt_idx": rank, "proof_solution": f"proof-{rank}"}]
                        if rank < 2
                        else []
                    ),
                    "failed_attempts": [],
                    "skipped_generations": [],
                    "cancelled_count": 0,
                },
            }
            for rank in range(4)
        ]

        merged = run.merge_distributed_pipeline_results(
            payloads,
            pipelines_per_problem=2,
            world_size=4,
        )

        self.assertEqual(
            [candidate["attempt_idx"] for candidate in merged["candidates"]],
            [0, 1],
        )

    def test_local_vllm_child_does_not_inherit_external_node_world(self):
        with tempfile.TemporaryDirectory() as temporary:
            cfg = SimpleNamespace(
                model_path="/model",
                served_model_name="proof-model",
                api_key="key",
                tensor_parallel_size=2,
                data_parallel_size=4,
                max_num_seqs=32,
                gpu_memory_utilization=0.95,
                host="127.0.0.1",
                dtype="auto",
                num_ctx=262_144,
                stream_interval=100,
                vllm_extra_args="",
                logdir=Path(temporary),
            )
            server = run.VLLMServer(
                cfg,
                port=8000,
                gpu_group="0,1,2,3,4,5,6,7",
                index=0,
            )
            fake_process = SimpleNamespace(poll=lambda: 0)
            with (
                patch.object(server, "is_port_open", return_value=False),
                patch.dict(
                    os.environ,
                    {
                        "GLOBAL_RANK": "5",
                        "WORLD_SIZE": "8",
                        "MASTER_ADDR": "10.0.0.1",
                        "MASTER_PORT": "29500",
                    },
                ),
                patch.object(subprocess, "Popen", return_value=fake_process) as popen,
            ):
                server.start()
                child_env = popen.call_args.kwargs["env"]
                server.stop()

        for key in ("GLOBAL_RANK", "WORLD_SIZE", "MASTER_ADDR", "MASTER_PORT"):
            self.assertNotIn(key, child_env)
        self.assertEqual(child_env["CUDA_VISIBLE_DEVICES"], "0,1,2,3,4,5,6,7")

    def test_two_rank_mock_run_writes_one_primary_output(self):
        try:
            import torch.distributed as dist
        except ImportError:
            self.skipTest("torch.distributed is unavailable")
        if not dist.is_available():
            self.skipTest("torch.distributed is unavailable")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "input.csv"
            output_path = root / "submission.csv"
            input_path.write_text(
                'id,problem\n1,"Prove the mock claim."\n', encoding="utf-8"
            )
            port = free_tcp_port()
            launcher = textwrap.dedent(
                """
                import os
                from pathlib import Path
                from evaluation.harness_vllm import run

                run.CFG.model_path = Path('/unused-model')
                run.CFG.input_csv = Path(os.environ['TEST_INPUT'])
                run.CFG.output_csv = Path(os.environ['AIMO_OUTPUT_PATH'])
                run.CFG.logdir = Path(os.environ['AIMO_LOGDIR'])
                run.CFG.mock_llm = True
                run.CFG.verbose = False
                run.CFG.num_gpus = 1
                run.CFG.gpus = '0'
                run.CFG.tensor_parallel_size = 1
                run.CFG.data_parallel_size = 1
                run.CFG.pipelines_per_problem = 4
                run.CFG.deepseek_math_v2_candidate_count = 0
                run.CFG.verify_n = 1
                run.CFG.meta_n = 0
                run.CFG.refine_rounds = 0
                run.CFG.selector_mode = 'score'
                run.CFG.max_rows = 1
                run.CFG.max_concurrent_problems = 1
                run.run()
                """
            )
            processes = []
            for rank in range(2):
                env = {
                    **os.environ,
                    "PYTHONPATH": str(REPO),
                    "GLOBAL_RANK": str(rank),
                    "WORLD_SIZE": "2",
                    "MASTER_ADDR": "127.0.0.1",
                    "MASTER_PORT": str(port),
                    "AIMO_DISTRIBUTED_ROOT": str(root / "distributed"),
                    "AIMO_DISTRIBUTED_RUN_ID": "mock-two-rank",
                    "AIMO_DISTRIBUTED_TIMEOUT_SECONDS": "60",
                    "AIMO_DISTRIBUTED_POLL_SECONDS": "0.1",
                    "AIMO_LOGDIR": str(root / "logs"),
                    "AIMO_OUTPUT_PATH": str(output_path),
                    "TEST_INPUT": str(input_path),
                }
                processes.append(
                    subprocess.Popen(
                        [sys.executable, "-c", launcher],
                        cwd=REPO,
                        env=env,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                    )
                )

            outputs = []
            for process in processes:
                output, _ = process.communicate(timeout=60)
                outputs.append(output)
            for rank, (process, output) in enumerate(zip(processes, outputs)):
                self.assertEqual(process.returncode, 0, f"rank={rank}\n{output}")

            with output_path.open(newline="", encoding="utf-8") as source:
                rows = list(csv.DictReader(source))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["id"], "1")
            self.assertIn("mock proof", rows[0]["answer"])

            problem_dir = next(
                (root / "distributed" / "runs" / "mock-two-rank" / "problems").iterdir()
            )
            payloads = [
                json.loads((problem_dir / f"rank_{rank:04d}.json").read_text())
                for rank in range(2)
            ]
            self.assertEqual(payloads[0]["assigned_attempts"], [0, 2])
            self.assertEqual(payloads[1]["assigned_attempts"], [1, 3])

    def test_startup_config_mismatch_fails_every_rank_without_deadlock(self):
        try:
            import torch.distributed as dist
        except ImportError:
            self.skipTest("torch.distributed is unavailable")
        if not dist.is_available():
            self.skipTest("torch.distributed is unavailable")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            port = free_tcp_port()
            launcher = textwrap.dedent(
                """
                import os
                from evaluation.harness_vllm import run

                distributed = run.DistributedRuntime.from_environment()
                distributed.initialize({"rank_specific": os.environ["GLOBAL_RANK"]})
                """
            )
            processes = []
            for rank in range(2):
                env = {
                    **os.environ,
                    "PYTHONPATH": str(REPO),
                    "GLOBAL_RANK": str(rank),
                    "WORLD_SIZE": "2",
                    "MASTER_ADDR": "127.0.0.1",
                    "MASTER_PORT": str(port),
                    "AIMO_DISTRIBUTED_ROOT": str(root / "distributed"),
                    "AIMO_DISTRIBUTED_RUN_ID": "mismatched-config",
                }
                processes.append(
                    subprocess.Popen(
                        [sys.executable, "-c", launcher],
                        cwd=REPO,
                        env=env,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                    )
                )

            outputs = [process.communicate(timeout=30)[0] for process in processes]
            for process, output in zip(processes, outputs):
                self.assertNotEqual(process.returncode, 0, output)
                self.assertIn("startup validation failed", output)


if __name__ == "__main__":
    unittest.main()
