from __future__ import annotations

import hashlib
import json
import os
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from evaluation.harness_vllm import run  # noqa: E402


class RunOpdPromptContractTests(unittest.TestCase):
    def test_parquet_input_is_supported(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "problems.parquet"
            run.pd.DataFrame(
                {
                    "problem_idx": [1, 2],
                    "problem": ["Prove the first claim.", "Prove the second claim."],
                }
            ).to_parquet(input_path)
            frame, problem_column, id_column = run.load_simple_input(input_path)

        self.assertEqual(len(frame), 2)
        self.assertEqual(problem_column, "problem")
        self.assertEqual(id_column, "problem_idx")

    def test_long_context_defaults_stay_near_training_length(self):
        self.assertEqual(run.CFG.num_ctx, 262_144)
        self.assertIn("--quantization fp8", run.CFG.vllm_extra_args)
        self.assertEqual(run.CFG.gpu_memory_utilization, 0.92)
        vllm_args = shlex.split(run.CFG.vllm_extra_args)
        self.assertEqual(
            vllm_args[vllm_args.index("--max-num-batched-tokens") + 1],
            "16384",
        )
        self.assertLessEqual(run.CFG.max_new_tokens, 131_072)
        self.assertGreaterEqual(min(run.CFG.proof_generation_thinking_budgets), 120_000)
        self.assertLess(
            max(run.CFG.proof_generation_thinking_budgets),
            run.CFG.max_new_tokens,
        )
        self.assertEqual(
            run.CFG.thinking_budget_force_text,
            "\n</think>\n\n<solution>\n"
            "We were unable to produce a complete proof. However, the strongest "
            "partial progress is as follows:\n",
        )
        self.assertEqual(run.CFG.verifier_max_new_tokens, 126_000)
        self.assertEqual(run.CFG.meta_max_new_tokens, 126_000)
        self.assertLess(
            run.CFG.verifier_thinking_budget_tokens,
            run.CFG.verifier_max_new_tokens,
        )
        self.assertLess(
            run.CFG.meta_thinking_budget_tokens,
            run.CFG.meta_max_new_tokens,
        )

    def test_dflash_can_be_enabled_from_environment(self):
        with patch.dict(
            os.environ,
            {
                "AIMO_DFLASH_MODEL_PATH": "/draft",
                "AIMO_DFLASH_NUM_SPECULATIVE_TOKENS": "10",
            },
        ):
            args = shlex.split(run.default_vllm_extra_args())

        config_index = args.index("--speculative-config") + 1
        self.assertEqual(
            json.loads(args[config_index]),
            {
                "method": "dflash",
                "model": "/draft",
                "num_speculative_tokens": 10,
                "disable_above_context_len": 65536,
            },
        )

    def test_max_num_batched_tokens_can_be_overridden(self):
        with patch.dict(
            os.environ,
            {"AIMO_MAX_NUM_BATCHED_TOKENS": "32768"},
        ):
            args = shlex.split(run.default_vllm_extra_args())

        self.assertEqual(
            args[args.index("--max-num-batched-tokens") + 1],
            "32768",
        )

    def test_tp2_dp4_auto_selects_eight_gpus(self):
        cfg = SimpleNamespace(
            gpus="",
            num_gpus=1,
            tensor_parallel_size=2,
            data_parallel_size=4,
        )

        selected_gpus, tp_size, dp_size = run.resolve_gpu_parallel_layout(cfg)

        self.assertEqual(selected_gpus, [str(index) for index in range(8)])
        self.assertEqual(tp_size, 2)
        self.assertEqual(dp_size, 4)

    def test_parallel_layout_infers_tp_from_explicit_gpus(self):
        cfg = SimpleNamespace(
            gpus="0,1,2,3,4,5,6,7",
            num_gpus=1,
            tensor_parallel_size=0,
            data_parallel_size=4,
        )

        selected_gpus, tp_size, dp_size = run.resolve_gpu_parallel_layout(cfg)

        self.assertEqual(len(selected_gpus), 8)
        self.assertEqual(tp_size, 2)
        self.assertEqual(dp_size, 4)

    def test_parallel_layout_rejects_incomplete_gpu_group(self):
        cfg = SimpleNamespace(
            gpus="0,1,2,3,4,5,6",
            num_gpus=1,
            tensor_parallel_size=2,
            data_parallel_size=4,
        )

        with self.assertRaisesRegex(ValueError, "GPU count must equal TP x DP"):
            run.resolve_gpu_parallel_layout(cfg)

    def test_request_concurrency_scales_with_selected_gpu_count(self):
        cfg = SimpleNamespace(
            max_concurrent_requests=0,
            requests_per_gpu=32,
        )

        self.assertEqual(run.resolve_max_concurrent_requests(cfg, 8), 256)

    def test_request_concurrency_supports_explicit_override(self):
        cfg = SimpleNamespace(
            max_concurrent_requests=96,
            requests_per_gpu=32,
        )

        self.assertEqual(run.resolve_max_concurrent_requests(cfg, 8), 96)

    def test_request_concurrency_rejects_invalid_values(self):
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            run.resolve_max_concurrent_requests(
                SimpleNamespace(
                    max_concurrent_requests=-1,
                    requests_per_gpu=32,
                ),
                8,
            )
        with self.assertRaisesRegex(ValueError, "must be at least 1"):
            run.resolve_max_concurrent_requests(
                SimpleNamespace(
                    max_concurrent_requests=0,
                    requests_per_gpu=0,
                ),
                8,
            )

    def test_vllm_command_forwards_data_parallel_size(self):
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
            logdir=REPO / "outputs" / "test-logs",
        )

        command = run.VLLMServer(
            cfg,
            port=8000,
            gpu_group="0,1,2,3,4,5,6,7",
            index=0,
        ).build_command()

        self.assertEqual(command[command.index("--tensor-parallel-size") + 1], "2")
        self.assertEqual(command[command.index("--data-parallel-size") + 1], "4")

    def test_dflash_disables_unsupported_min_p(self):
        with patch.dict(os.environ, {"AIMO_DFLASH_MODEL_PATH": "/draft"}):
            self.assertIsNone(run.default_min_p())
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(run.default_min_p(), 0.01)

    def test_imo2025_defaults_run_the_complete_candidate_pipeline(self):
        self.assertEqual(
            run.CFG.input_csv,
            REPO / "test.csv",
        )
        self.assertEqual(run.CFG.pipelines_per_problem, 14)
        self.assertEqual(run.CFG.deepseek_math_v2_candidate_count, 6)
        self.assertEqual(run.CFG.proof_only_candidate_count, 0)
        self.assertFalse(run.CFG.skip_self_score_zero)
        self.assertFalse(run.CFG.stop_on_strict_pass)
        self.assertFalse(run.CFG.verification_early_stop)
        self.assertEqual(run.CFG.verify_n, 4)
        self.assertEqual(run.CFG.meta_n, 1)
        self.assertEqual(run.CFG.meta_policy, "all-reviews")
        self.assertEqual(run.CFG.refine_rounds, 1)
        self.assertEqual(run.CFG.refine_review_n, 2)
        self.assertLess(run.CFG.refine_review_n, run.CFG.verify_n)
        self.assertGreaterEqual(run.CFG.problem_timeout_seconds, 86_400)

    def test_prover_uses_trained_system_user_prompt(self):
        messages = run.build_opd_proof_generation_prompt("Prove the claim.")

        self.assertEqual([message["role"] for message in messages], ["system", "user"])
        self.assertIn("mathematical proof generator", messages[0]["content"])
        self.assertIn(
            "Do not repeat yourself or brute-force a solution.",
            messages[0]["content"],
        )
        self.assertIn("Problem:\nProve the claim.", messages[1]["content"])
        self.assertIn("<self_evaluation>", messages[1]["content"])

    def test_generation_parser_reads_opd_xml(self):
        parsed = run.parse_generation_response(
            "<think>private work</think>"
            "<solution>A complete proof.</solution>"
            "<self_evaluation>The proof is checked.</self_evaluation>"
            "<score>1</score>"
        )

        self.assertTrue(parsed["is_valid_candidate_response"])
        self.assertEqual(parsed["proof"], "A complete proof.")
        self.assertEqual(parsed["self_score"], 1.0)

    def test_deepseek_prompt_and_generation_parser_use_markdown_contract(self):
        prompt = run.build_deepseek_proof_generation_prompt("Prove the claim.")
        parsed = run.parse_deepseek_generation_response(
            "<think>private work</think>\n"
            "## Solution\nA complete proof.\n\n"
            "## Self Evaluation\n"
            "Here is my evaluation of the solution: It is complete.\n"
            "Based on my evaluation, the final overall score should be:\n"
            "\\boxed{1}"
        )

        self.assertIn("## Solution", prompt)
        self.assertIn("## Self Evaluation", prompt)
        self.assertIn("## Problem\nProve the claim.", prompt)
        self.assertTrue(parsed["is_valid_candidate_response"])
        self.assertEqual(parsed["proof"], "A complete proof.")
        self.assertEqual(parsed["self_score"], 1.0)

    def test_deepseek_verifier_parser_normalizes_current_schema(self):
        prompt = run.build_deepseek_proof_verification_prompt(
            "Problem.",
            "Candidate proof.",
        )
        parsed = run.parse_deepseek_verifier_response(
            "<think>private work</think>\n"
            "Here is my evaluation of the solution:\nA fatal gap remains.\n\n"
            "Based on my evaluation, the final overall score should be:\n"
            "\\boxed{0}"
        )

        self.assertIn("## Solution\nCandidate proof.", prompt)
        self.assertTrue(parsed["is_valid_verifier_response"])
        self.assertEqual(parsed["score"], 0.0)
        self.assertEqual(parsed["evaluation"], "A fatal gap remains.")
        self.assertIn("Here is my evaluation", parsed["review"])

    def test_first_six_candidates_use_deepseek_prompt_family(self):
        cfg = SimpleNamespace(deepseek_math_v2_candidate_count=6)

        families = [
            run.resolve_candidate_prompt_family(index, 14, cfg) for index in range(14)
        ]

        self.assertEqual(
            families,
            [run.PROMPT_FAMILY_DEEPSEEK_MATH_V2] * 6 + [run.PROMPT_FAMILY_OPD] * 8,
        )
        all_opd = SimpleNamespace(deepseek_math_v2_candidate_count=0)
        all_deepseek = SimpleNamespace(deepseek_math_v2_candidate_count=14)
        self.assertEqual(
            run.resolve_candidate_prompt_family(0, 14, all_opd),
            run.PROMPT_FAMILY_OPD,
        )
        self.assertEqual(
            run.resolve_candidate_prompt_family(13, 14, all_deepseek),
            run.PROMPT_FAMILY_DEEPSEEK_MATH_V2,
        )
        with self.assertRaisesRegex(ValueError, "between 0"):
            run.resolve_candidate_prompt_family(
                0,
                14,
                SimpleNamespace(deepseek_math_v2_candidate_count=15),
            )

    def test_reasoning_repetition_metrics_use_hidden_reasoning_only(self):
        words = [f"word{index}" for index in range(32)] * 3
        text = (
            "<think>"
            + " ".join(words)
            + "</think><solution>Visible output is excluded.</solution>"
        )

        metrics = run.measure_reasoning_repetition(text)

        self.assertEqual(metrics["word_count"], 96)
        self.assertEqual(metrics["window_words"], 32)
        self.assertEqual(metrics["word_window_count"], 65)
        self.assertEqual(metrics["repeated_word_window_count"], 33)
        self.assertAlmostEqual(metrics["repeated_word_window_fraction"], 33 / 65)
        self.assertGreater(metrics["gzip_factor"], 1.0)

    def test_reasoning_repetition_supports_orphan_think_close(self):
        metrics = run.measure_reasoning_repetition(
            "private hidden work</think><solution>Visible.</solution>"
        )

        self.assertEqual(metrics["word_count"], 3)
        self.assertEqual(metrics["word_window_count"], 0)
        self.assertEqual(metrics["repeated_word_window_fraction"], 0.0)

    def test_proof_output_carries_reasoning_repetition_metrics(self):
        response = {
            "stage": "proof_generation",
            "success": True,
            "text": "<think>private work</think><solution>Proof.</solution>",
        }
        response["reasoning_repetition"] = run.measure_reasoning_repetition(
            response["text"]
        )

        output = run.make_output("proof_generation", response, {})

        self.assertEqual(output["reasoning_repetition"]["word_count"], 2)

    def test_verifier_requires_complete_xml_contract(self):
        valid = run.parse_verifier_response(
            "<evaluation>A fatal gap exists.</evaluation>"
            "<suggestions>Prove the missing lemma.</suggestions>"
            "<score>0</score>"
        )
        malformed = run.parse_verifier_response(
            "<evaluation>Claims to pass.</evaluation><score>1</score>"
        )

        self.assertTrue(valid["is_valid_verifier_response"])
        self.assertEqual(valid["score"], 0.0)
        self.assertFalse(malformed["is_valid_verifier_response"])
        self.assertIsNone(malformed["score"])

    def test_refiner_receives_xml_candidate_and_reviews(self):
        messages = run.build_opd_proof_refinement_prompt(
            "Problem.",
            "P3",
            "Candidate proof.",
            "Candidate audit.",
            [
                {
                    "score": 0.5,
                    "review": (
                        "<evaluation>Minor gap.</evaluation>"
                        "<suggestions>Fill it.</suggestions><score>0.5</score>"
                    ),
                }
            ],
        )
        user = messages[1]["content"]

        self.assertIn('<candidate id="P3">', user)
        self.assertIn('<verifier_review score="0.5">', user)
        self.assertIn("Candidate audit.", user)

    def test_selector_uses_trained_id_contract(self):
        messages = run.build_selection_prompt(
            "Problem.",
            [{"proof_solution": "First."}, {"proof_solution": "Second."}],
            10_000,
        )

        self.assertEqual(
            hashlib.sha256(
                (run.OPD_PROMPT_ROOT / "selector.txt").read_bytes()
            ).hexdigest(),
            "1cf13bb2c62cc15b3f92b4d65a5e25e8893736d6cc3afb49f01a49c13b45052b",
        )
        self.assertIn('<candidate id="R0">', messages[1]["content"])
        self.assertEqual(
            run.parse_selected_index("<selected_id>R1</selected_id>", 2), 1
        )
        self.assertIsNone(run.parse_selected_index("SELECTED_INDEX: 1", 2))

    def test_only_requested_deepseek_prompt_branches_are_retained(self):
        self.assertTrue(hasattr(run, "build_deepseek_proof_generation_prompt"))
        self.assertTrue(hasattr(run, "build_deepseek_proof_verification_prompt"))
        self.assertTrue(hasattr(run, "build_deepseek_meta_verification_prompt"))
        self.assertFalse(hasattr(run, "build_deepseek_gold_proof_evaluation_prompt"))
        self.assertFalse(hasattr(run, "build_proof_architect_prompt"))
        self.assertFalse(hasattr(run, "build_sublemma_prover_prompt"))

    def test_grader_input_uses_full_proofs_and_omits_failed_rows(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "grader_input" / "records.jsonl"
            full_proof = "A" * (run.MAX_SUBMISSION_ANSWER_CHARS + 100)
            run.write_grader_input_records(
                path,
                [
                    {
                        "id": 1,
                        "answer": full_proof[: run.MAX_SUBMISSION_ANSWER_CHARS],
                        "prediction": full_proof,
                        "selected_pipeline": 3,
                        "final_score": 0.75,
                        "final_status": "refined",
                        "error": "",
                    },
                    {
                        "id": 2,
                        "prediction": "Fallback proof",
                        "final_status": "all_attempts_failed",
                        "error": "",
                    },
                ],
            )

            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["problem_id"], "1")
            self.assertEqual(records[0]["final_proof"], full_proof)
            self.assertEqual(records[0]["selected_pipeline"], 3)
            self.assertFalse(path.with_suffix(".jsonl.tmp").exists())


class MixedPromptRoutingTests(unittest.IsolatedAsyncioTestCase):
    async def test_generation_dispatches_prompt_parser_and_force_text_by_family(self):
        class FakeScheduler:
            def __init__(self) -> None:
                self.calls: list[tuple[object, dict[str, object]]] = []

            async def call(self, stage: str, prompt: object, **kwargs: object):
                self.assert_stage(stage)
                self.calls.append((prompt, kwargs))
                if isinstance(prompt, str):
                    text = (
                        "## Solution\nDeepSeek proof.\n\n"
                        "## Self Evaluation\nChecked.\n\\boxed{1}"
                    )
                else:
                    text = (
                        "<solution>OPD proof.</solution>"
                        "<self_evaluation>Checked.</self_evaluation>"
                        "<score>1</score>"
                    )
                return {"success": True, "text": text}

            @staticmethod
            def assert_stage(stage: str) -> None:
                if stage != "proof_generation":
                    raise AssertionError(stage)

        cfg = SimpleNamespace(
            deepseek_math_v2_candidate_count=6,
            thinking_budget_enabled=False,
            proof_generation_thinking_budgets=[],
            default_temperature=0.7,
            proof_generation_temperatures=[],
            deepseek_thinking_budget_force_text="## Solution\n",
            thinking_budget_force_text="<solution>\n",
        )
        scheduler = FakeScheduler()

        deepseek = await run.generate_single_attempt("Problem.", 0, 14, scheduler, cfg)
        opd = await run.generate_single_attempt("Problem.", 6, 14, scheduler, cfg)

        self.assertEqual(
            deepseek["prompt_family"],
            run.PROMPT_FAMILY_DEEPSEEK_MATH_V2,
        )
        self.assertEqual(opd["prompt_family"], run.PROMPT_FAMILY_OPD)
        self.assertIsInstance(scheduler.calls[0][0], str)
        self.assertIsInstance(scheduler.calls[1][0], list)
        self.assertEqual(
            scheduler.calls[0][1]["thinking_budget_force_text"],
            "## Solution\n",
        )
        self.assertEqual(
            scheduler.calls[1][1]["thinking_budget_force_text"],
            "<solution>\n",
        )

    async def test_deepseek_candidate_keeps_deepseek_verifier_after_opd_refine(self):
        class FakeScheduler:
            def __init__(self) -> None:
                self.calls: list[tuple[str, object]] = []
                self.responses = iter(
                    [
                        (
                            "Here is my evaluation of the solution:\n"
                            "A key justification is missing.\n\n"
                            "Based on my evaluation, the final overall score "
                            "should be:\n\\boxed{0}"
                        ),
                        (
                            "<solution>A repaired complete proof.</solution>"
                            "<self_evaluation>The gap is now filled.</self_evaluation>"
                            "<score>1</score>"
                        ),
                        (
                            "Here is my evaluation of the solution:\n"
                            "The repaired proof is complete.\n\n"
                            "Based on my evaluation, the final overall score "
                            "should be:\n\\boxed{1}"
                        ),
                    ]
                )

            async def call(self, stage: str, prompt: object, **kwargs: object):
                del kwargs
                self.calls.append((stage, prompt))
                return {
                    "success": True,
                    "error": None,
                    "text": next(self.responses),
                    "finish_reason": "stop",
                    "usage": {},
                    "server_url": "mock",
                    "latency_s": 0.0,
                }

        initial_text = (
            "## Solution\nAn incomplete proof.\n\n"
            "## Self Evaluation\nHere is my evaluation of the solution: "
            "a gap remains.\n\\boxed{0}"
        )
        initial_parsed = run.parse_deepseek_generation_response(initial_text)
        initial_generation = {
            "attempt_idx": 0,
            "prompt_family": run.PROMPT_FAMILY_DEEPSEEK_MATH_V2,
            "generation_mode": "deepseek_markdown",
            "generation_output": run.make_output(
                "proof_generation",
                {"success": True, "text": initial_text},
                initial_parsed,
                prompt_family=run.PROMPT_FAMILY_DEEPSEEK_MATH_V2,
            ),
            "generation_parsed": initial_parsed,
            "proof": initial_parsed["proof"],
        }
        cfg = SimpleNamespace(
            verify_n=1,
            meta_n=0,
            meta_policy="all-reviews",
            strict_pass_meta=False,
            refine_rounds=1,
            refine_review_n=1,
            min_valid_low=1,
            verification_early_stop=False,
            thinking_budget_enabled=False,
            verifier_thinking_budget_tokens=0,
            verifier_thinking_budget_force_text="<evaluation>\n",
            deepseek_verifier_thinking_budget_force_text=(
                "Here is my evaluation of the solution:\n"
            ),
            meta_thinking_budget_tokens=0,
            meta_thinking_budget_force_text="",
        )
        scheduler = FakeScheduler()

        result = await run.run_single_attempt(
            "Problem.",
            0,
            14,
            scheduler,
            cfg,
            initial_generation=initial_generation,
        )

        self.assertEqual(
            [stage for stage, _ in scheduler.calls],
            ["proof_verify", "proof_refine", "proof_verify"],
        )
        self.assertIsInstance(scheduler.calls[0][1], str)
        self.assertIsInstance(scheduler.calls[1][1], list)
        self.assertIsInstance(scheduler.calls[2][1], str)
        self.assertIn("## Instruction", str(scheduler.calls[0][1]))
        self.assertIn("## Instruction", str(scheduler.calls[2][1]))
        self.assertIn(
            '<candidate id="P0">',
            scheduler.calls[1][1][1]["content"],
        )
        self.assertEqual(
            result["prompt_family"],
            run.PROMPT_FAMILY_DEEPSEEK_MATH_V2,
        )
        self.assertEqual(result["proof_solution"], "A repaired complete proof.")


if __name__ == "__main__":
    unittest.main()
