from __future__ import annotations

import asyncio
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

from proof_prompts import (  # noqa: E402
    generation_messages,
    parse_generation,
    parse_verification,
    prompt_hashes,
    refinement_messages,
)
from proof_search import ProblemSearch, Proof, Verification  # noqa: E402


class ScriptedClient:
    def __init__(self, *, stop_after_first_round: bool = False):
        self.stop_after_first_round = stop_after_first_round
        self.calls: list[str] = []
        self.kwargs: list[dict] = []
        self.messages: dict[str, list[dict[str, str]]] = {}

    async def chat_raw(self, messages, *, request_id, **kwargs):
        self.calls.append(request_id)
        self.kwargs.append(kwargs)
        self.messages[request_id] = messages
        if "/verify/" in request_id:
            score = 1 if self.stop_after_first_round or "round-02" in request_id else 0.5
            content = (
                f"<evaluation>The argument is checked for {request_id}.</evaluation>\n"
                "<suggestions>Make every equality explicit.</suggestions>\n"
                f"<score>{score}</score>"
            )
        else:
            content = (
                "<solution>"
                f"A rigorous proof generated for {request_id}."
                "</solution>\n"
                "<self_evaluation>All stated steps are justified.</self_evaluation>\n"
                "<score>1</score>"
            )
        return {
            "message": {"content": content, "reasoning_content": "reasoning"},
            "finish_reason": "stop",
            "prompt_tokens": 10,
            "cached_prompt_tokens": 9,
            "completion_tokens": 20,
            "reasoning_tokens": 5,
            "requested_max_completion_tokens": 100,
            "logical_max_completion_tokens": 100,
            "physical_request_count": 1,
            "physical_prompt_tokens": 10,
            "segments": [{"kind": "chat", "finish_reason": "stop"}],
            "latency_s": 0.01,
        }


class MalformedCandidateClient(ScriptedClient):
    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if "/generate/" in request_id and request_id.endswith("p0000"):
            response["message"]["content"] = "No XML candidate."
        return response


class LengthContinuationClient(ScriptedClient):
    def __init__(self, *, invalid_continuation: bool = False):
        super().__init__()
        self.invalid_continuation = invalid_continuation
        self.continuation_calls: list[dict] = []

    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if "/generate/" not in request_id or not request_id.endswith("p0000"):
            return response
        response.update(
            finish_reason="length",
            completion_tokens=kwargs["max_completion_tokens"],
            requested_max_completion_tokens=kwargs["max_completion_tokens"],
            logical_max_completion_tokens=kwargs["max_completion_tokens"],
            physical_request_count=1,
            physical_prompt_tokens=10,
            segments=[{"kind": "chat", "finish_reason": "length"}],
        )
        response["message"] = {
            "content": "",
            "reasoning_content": "private unfinished reasoning",
        }
        return response

    async def continue_solution_raw(self, initial, messages, **kwargs):
        self.continuation_calls.append({"messages": messages, **kwargs})
        content = (
            "<solution>unfinished"
            if self.invalid_continuation
            else (
                "<solution>Recovered proof.</solution>\n"
                "<self_evaluation>Recovered and checked.</self_evaluation>\n"
                "<score>1</score>"
            )
        )
        return {
            **initial,
            "message": {
                "content": content,
                "reasoning_content": initial["message"]["reasoning_content"],
            },
            "finish_reason": "stop",
            "completion_tokens": (
                initial["completion_tokens"] + kwargs["max_new_tokens"]
            ),
            "requested_solution_continuation_tokens": kwargs["max_new_tokens"],
            "logical_max_completion_tokens": (
                initial["requested_max_completion_tokens"]
                + kwargs["max_new_tokens"]
            ),
            "physical_request_count": 2,
            "physical_prompt_tokens": 150,
            "segments": [
                *initial["segments"],
                {"kind": "solution_continuation", "finish_reason": "stop"},
            ],
            "latency_s": initial["latency_s"] + 0.02,
        }


class CompleteXMLAtLengthClient(ScriptedClient):
    def __init__(self):
        super().__init__()
        self.continuation_calls = 0

    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if "/generate/" in request_id and request_id.endswith("p0000"):
            response.update(
                finish_reason="length",
                physical_request_count=1,
                segments=[{"kind": "chat", "finish_reason": "length"}],
            )
        return response

    async def continue_solution_raw(self, initial, messages, **kwargs):
        self.continuation_calls += 1
        raise AssertionError("complete XML must not receive a continuation")


class LengthVerifierContinuationClient(ScriptedClient):
    def __init__(self, *, invalid_continuation: bool = False):
        super().__init__()
        self.invalid_continuation = invalid_continuation
        self.verifier_continuation_calls: list[dict] = []

    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if not request_id.endswith("/r01-p0000/v000"):
            return response
        response.update(
            finish_reason="length",
            completion_tokens=kwargs["max_completion_tokens"],
            requested_max_completion_tokens=kwargs["max_completion_tokens"],
            logical_max_completion_tokens=kwargs["max_completion_tokens"],
            physical_request_count=1,
            physical_prompt_tokens=10,
            segments=[{"kind": "chat", "finish_reason": "length"}],
        )
        response["message"] = {
            "content": "",
            "reasoning_content": "private verifier reasoning",
        }
        return response

    async def continue_verification_raw(self, initial, messages, **kwargs):
        self.verifier_continuation_calls.append({"messages": messages, **kwargs})
        content = (
            "<evaluation>unfinished"
            if self.invalid_continuation
            else (
                "<evaluation>Recovered review.</evaluation>\n"
                "<suggestions>No repairs.</suggestions>\n"
                "<score>0.5</score>"
            )
        )
        return {
            **initial,
            "message": {
                "content": content,
                "reasoning_content": initial["message"]["reasoning_content"],
            },
            "finish_reason": "stop",
            "completion_tokens": (
                initial["completion_tokens"] + kwargs["max_new_tokens"]
            ),
            "requested_verifier_continuation_tokens": kwargs["max_new_tokens"],
            "logical_max_completion_tokens": (
                initial["requested_max_completion_tokens"]
                + kwargs["max_new_tokens"]
            ),
            "physical_request_count": 2,
            "physical_prompt_tokens": 150,
            "segments": [
                *initial["segments"],
                {"kind": "verifier_continuation", "finish_reason": "stop"},
            ],
            "latency_s": initial["latency_s"] + 0.02,
        }


class CompleteVerifierXMLAtLengthClient(ScriptedClient):
    def __init__(self):
        super().__init__()
        self.verifier_continuation_calls = 0

    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if request_id.endswith("/r01-p0000/v000"):
            response.update(
                finish_reason="length",
                physical_request_count=1,
                segments=[{"kind": "chat", "finish_reason": "length"}],
            )
        return response

    async def continue_verification_raw(self, initial, messages, **kwargs):
        self.verifier_continuation_calls += 1
        raise AssertionError("complete verifier XML must not receive a continuation")


class MalformedVerifierClient(ScriptedClient):
    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if request_id.endswith("/v000"):
            response["message"]["content"] = "No XML verification."
        return response


class AllMalformedVerifierClient(ScriptedClient):
    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if "/verify/" in request_id:
            response["message"]["content"] = "No XML verification."
        return response


class AsyncPipelineClient(ScriptedClient):
    def __init__(self, *, expected_generations: int, concurrency: int):
        super().__init__()
        self.expected_generations = expected_generations
        self.concurrency = concurrency
        self.generation_starts = 0
        self.active = 0
        self.max_active = 0
        self.all_generations_started = asyncio.Event()
        self.verifier_started = asyncio.Event()
        self.saturated = asyncio.Event()
        self.release = asyncio.Event()

    async def chat_raw(self, messages, *, request_id, **kwargs):
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        if self.active == self.concurrency:
            self.saturated.set()
        try:
            response = await super().chat_raw(
                messages, request_id=request_id, **kwargs
            )
            if "/generate/" in request_id:
                self.generation_starts += 1
                if self.generation_starts == self.expected_generations:
                    self.all_generations_started.set()
                if request_id.endswith(
                    f"p{self.expected_generations - 1:04d}"
                ):
                    await self.release.wait()
            else:
                self.verifier_started.set()
                await self.release.wait()
            return response
        finally:
            self.active -= 1


class BlockingVerifierClient(ScriptedClient):
    def __init__(self, blocked_request_id: str):
        super().__init__()
        self.blocked_request_id = blocked_request_id
        self.blocked_started = asyncio.Event()
        self.release = asyncio.Event()

    async def chat_raw(self, messages, *, request_id, **kwargs):
        response = await super().chat_raw(
            messages, request_id=request_id, **kwargs
        )
        if request_id == self.blocked_request_id:
            self.blocked_started.set()
            await self.release.wait()
        return response


def small_config() -> dict:
    return {
        "proofs_per_round": 2,
        "verifications_per_proof": 2,
        "top_proofs": 1,
        "refinements_per_proof": 2,
        "analyses_per_refinement": 2,
        "max_rounds": 2,
        "early_stop_threshold": 0.99999,
        "temperature": 1.0,
        "top_p": 0.95,
        "max_completion_tokens": 128,
        "solution_continuation_tokens": 64,
        "verifier_continuation_tokens": 64,
        "min_valid_verifications": 2,
        "concurrency": 4,
        "seed": 17,
    }


class ProofSearchTests(unittest.TestCase):
    def test_async_pipeline_overlaps_generation_and_verification_at_64(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config.update(
                    proofs_per_round=32,
                    verifications_per_proof=16,
                    max_rounds=1,
                    min_valid_verifications=4,
                    concurrency=64,
                )
                client = AsyncPipelineClient(
                    expected_generations=32, concurrency=64
                )
                search = ProblemSearch(
                    problem_id="1",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(64),
                    config=config,
                )

                task = asyncio.create_task(search.solve())
                await asyncio.wait_for(
                    client.all_generations_started.wait(), timeout=2
                )
                await asyncio.wait_for(client.verifier_started.wait(), timeout=2)
                await asyncio.wait_for(client.saturated.wait(), timeout=2)

                self.assertEqual(
                    client.calls[:32],
                    [
                        f"round-01/generate/r01-p{index:04d}"
                        for index in range(32)
                    ],
                )
                self.assertEqual(client.active, 64)
                self.assertEqual(client.max_active, 64)
                self.assertFalse(task.done())

                client.release.set()
                final = await asyncio.wait_for(task, timeout=10)

                self.assertEqual(final["proofs_in_pool"], 32)
                self.assertEqual(final["calls_completed"], 32 + 32 * 16)
                self.assertEqual(client.max_active, 64)

        asyncio.run(run())

    def test_prompt_files_are_byte_identical_to_ycchen_commit(self):
        self.assertEqual(
            prompt_hashes(),
            {
                "prover.txt": "2f464567b97288c0b934b3aed2e32bdb5cd612a04c33f3ad86839b87005d5d4c",
                "verifier.txt": "8c8e904270d6ae54d04aa8782d91f5eca94ccbc1c850bee0685b9a4668242dec",
                "refiner.txt": "0bc15f3fa590cc3970a5a65dd573ec3d31b39ad70a78179e5e06ac5b9654fb18",
            },
        )

    def test_ycchen_system_user_split_and_candidate_bundle(self):
        messages = generation_messages("Prove it.")
        self.assertEqual([message["role"] for message in messages], ["system", "user"])
        self.assertNotIn("===SYSTEM===", messages[0]["content"])
        self.assertIn("Problem:\nProve it.", messages[1]["content"])
        refined = refinement_messages(
            "Prove it.", "r01-p0000", "Candidate proof.", "Candidate audit.",
            0.0, "Fatal review.",
        )
        user = refined[1]["content"]
        self.assertIn('<candidate id="r01-p0000">', user)
        self.assertIn('<verifier_review score="0">\nFatal review.', user)
        self.assertEqual(user.count("<verifier_review "), 1)

    def test_lowest_reviews_are_selected_deterministically(self):
        with tempfile.TemporaryDirectory() as directory:
            config = small_config()
            config["analyses_per_refinement"] = 4
            config["refinements_per_proof"] = 4
            search = ProblemSearch(
                problem_id="1",
                problem="Prove the claim.",
                output_dir=Path(directory),
                client=ScriptedClient(),
                semaphore=asyncio.Semaphore(4),
                config=config,
            )
            proof = Proof(
                proof_id="r01-p0000",
                round_index=1,
                parent_id=None,
                proof="Proof.",
                self_evaluation="Audit.",
                self_score=1.0,
                generation_sample_id="generate",
                verifications=[
                    Verification(f"v{index}", score, f"Review {index}.")
                    for index, score in enumerate((1.0, 0.5, 0.0, 1.0, 0.5, 0.0))
                ],
            )
            selected = search._selected_reviews(proof, 2)
            repeated = search._selected_reviews(proof, 2)

        self.assertEqual([item.score for item in selected], [0.0, 0.0, 0.5, 0.5])
        self.assertEqual(
            [item.sample_id for item in selected],
            [item.sample_id for item in repeated],
        )

    def test_ranking_prefers_more_valid_votes_after_equal_mean(self):
        with tempfile.TemporaryDirectory() as directory:
            search = ProblemSearch(
                problem_id="1",
                problem="Prove the claim.",
                output_dir=Path(directory),
                client=ScriptedClient(),
                semaphore=asyncio.Semaphore(4),
                config=small_config(),
            )
            fewer = Proof(
                "fewer", 1, None, "Proof.", "Audit.", 1.0, "generate",
                [Verification(f"f{i}", 0.5, "Review.") for i in range(2)],
            )
            more = Proof(
                "more", 1, None, "Proof.", "Audit.", 0.0, "generate",
                [Verification(f"m{i}", 0.5, "Review.") for i in range(3)],
            )
            below_minimum = Proof(
                "below", 1, None, "Proof.", "Audit.", 1.0, "generate",
                [Verification("b0", 1.0, "Review.")],
            )
            search.proofs = {
                proof.proof_id: proof
                for proof in (fewer, more, below_minimum)
            }

            self.assertEqual(
                [proof.proof_id for proof in search.ranked()],
                ["more", "fewer"],
            )

    def test_strict_xml_response_parsers(self):
        proof, evaluation, score = parse_generation(
            "<solution>Proof.</solution>\n"
            "<self_evaluation>Audit.</self_evaluation>\n<score>0.5</score>"
        )
        self.assertEqual((proof, evaluation, score), ("Proof.", "Audit.", 0.5))
        verifier, verifier_score = parse_verification(
            "<evaluation>Valid.</evaluation>\n"
            "<suggestions>No repairs.</suggestions>\n<score>1</score>"
        )
        self.assertIn("<evaluation>Valid.</evaluation>", verifier)
        self.assertEqual(verifier_score, 1.0)
        with self.assertRaises(ValueError):
            parse_generation("unstructured")
        with self.assertRaises(ValueError):
            parse_verification("<evaluation>Evaluation only.</evaluation>")

    def test_refinement_parent_selection_uses_the_cumulative_pool(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                client = ScriptedClient()
                search = ProblemSearch(
                    problem_id="9",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=small_config(),
                )
                older = Proof(
                    proof_id="r01-p0000",
                    round_index=1,
                    parent_id=None,
                    proof="Older stronger proof.",
                    self_evaluation="Audit.",
                    self_score=1.0,
                    generation_sample_id="old-generate",
                    verifications=[
                        Verification(f"old-v{index}", 1.0, f"Old review {index}.")
                        for index in range(2)
                    ],
                )
                recent = Proof(
                    proof_id="r02-p0000",
                    round_index=2,
                    parent_id=older.proof_id,
                    proof="Recent weaker proof.",
                    self_evaluation="Audit.",
                    self_score=1.0,
                    generation_sample_id="new-generate",
                    verifications=[
                        Verification(f"new-v{index}", 0.5, f"New review {index}.")
                        for index in range(2)
                    ],
                )
                search.proofs = {older.proof_id: older, recent.proof_id: recent}

                generated, _ = await search._run_round(3)

                self.assertEqual([proof.parent_id for proof in generated], [older.proof_id] * 2)
                refinement_prompts = [
                    client.messages[request_id][1]["content"]
                    for request_id in client.calls
                    if request_id.startswith("round-03/generate/")
                ]
                self.assertTrue(
                    all(
                        f'<candidate id="{older.proof_id}">' in prompt
                        for prompt in refinement_prompts
                    )
                )

        asyncio.run(run())

    def test_resumed_round_excludes_partial_current_round_from_parents(self):
        with tempfile.TemporaryDirectory() as directory:
            search = ProblemSearch(
                problem_id="19",
                problem="Prove the claim.",
                output_dir=Path(directory),
                client=ScriptedClient(),
                semaphore=asyncio.Semaphore(4),
                config=small_config(),
            )
            previous = Proof(
                proof_id="r01-p0000",
                round_index=1,
                parent_id=None,
                proof="Completed previous-round proof.",
                self_evaluation="Audit.",
                self_score=1.0,
                generation_sample_id="r01-generate",
                verifications=[
                    Verification(f"r01-v{index}", 0.5, f"Review {index}.")
                    for index in range(2)
                ],
            )
            partial = Proof(
                proof_id="r02-p0000",
                round_index=2,
                parent_id=previous.proof_id,
                proof="Stronger partial current-round proof.",
                self_evaluation="Audit.",
                self_score=1.0,
                generation_sample_id="r02-generate",
                verifications=[
                    Verification(f"r02-v{index}", 1.0, f"Review {index}.")
                    for index in range(2)
                ],
            )
            search.proofs = {
                previous.proof_id: previous,
                partial.proof_id: partial,
            }

            candidates = search._round_candidates(2)

            self.assertEqual(
                [candidate.parent_id for candidate in candidates],
                [previous.proof_id, previous.proof_id],
            )

    def test_arbitrary_yaml_values_drive_two_round_search(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                client = ScriptedClient()
                search = ProblemSearch(
                    problem_id="1",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=small_config(),
                )
                final = await search.solve()
                self.assertEqual(final["rounds_completed"], 2)
                self.assertEqual(final["proofs_in_pool"], 4)
                self.assertEqual(final["calls_completed"], 12)
                self.assertTrue(final["selected_proof_id"].startswith("r02-"))
                self.assertEqual(len(client.calls), len(set(client.calls)))
                self.assertTrue(
                    all(
                        kwargs["max_completion_tokens"] == 128
                        for kwargs in client.kwargs
                    )
                )
                refinement_ids = [
                    request_id
                    for request_id in client.calls
                    if request_id.startswith("round-02/generate/")
                ]
                review_prompts = [
                    client.messages[request_id][1]["content"]
                    for request_id in refinement_ids
                ]
                self.assertEqual(len(review_prompts), 2)
                self.assertEqual(
                    [prompt.count("<verifier_review ") for prompt in review_prompts],
                    [1, 1],
                )
                self.assertEqual(len(set(review_prompts)), 2)

        asyncio.run(run())

    def test_round_checkpoints_follow_persisted_ranking_and_resume(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                config = small_config()
                config["early_stop_threshold"] = 1.0
                checkpoints = []

                async def checkpoint(value: dict) -> None:
                    summary_path = (
                        root
                        / "rounds"
                        / "round-{:02d}.json".format(value["round"])
                    )
                    self.assertTrue(summary_path.exists())
                    summary = json.loads(summary_path.read_text())
                    self.assertEqual(
                        summary["best_proof_id"], value["selected_proof_id"]
                    )
                    checkpoints.append(value)

                search = ProblemSearch(
                    problem_id="checkpoint",
                    problem="Prove the claim.",
                    output_dir=root,
                    client=ScriptedClient(),
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                    on_round_complete=checkpoint,
                )
                final = await search.solve()
                self.assertEqual(
                    [value["round"] for value in checkpoints], [1, 2]
                )
                self.assertEqual(
                    checkpoints[-1]["selected_proof_id"],
                    final["selected_proof_id"],
                )

                (root / "final.json").unlink()
                replayed = []

                async def replay(value: dict) -> None:
                    replayed.append(value)

                resumed_client = ScriptedClient()
                resumed = ProblemSearch(
                    problem_id="checkpoint",
                    problem="Prove the claim.",
                    output_dir=root,
                    client=resumed_client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                    on_round_complete=replay,
                )
                resumed_final = await resumed.solve()
                self.assertEqual(
                    [value["round"] for value in replayed], [2]
                )
                self.assertEqual(
                    replayed[0]["selected_proof_id"],
                    resumed_final["selected_proof_id"],
                )
                self.assertEqual(resumed_client.calls, [])

        asyncio.run(run())

    def test_next_round_waits_for_every_verifier_pipeline(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                blocked_id = "round-01/verify/r01-p0001/v001"
                client = BlockingVerifierClient(blocked_id)
                search = ProblemSearch(
                    problem_id="17",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=small_config(),
                )

                task = asyncio.create_task(search.solve())
                await asyncio.wait_for(client.blocked_started.wait(), timeout=1)
                await asyncio.sleep(0)

                self.assertFalse(
                    any(call.startswith("round-02/") for call in client.calls)
                )
                client.release.set()
                final = await asyncio.wait_for(task, timeout=2)

                self.assertEqual(final["rounds_completed"], 2)
                self.assertTrue(
                    any(call.startswith("round-02/") for call in client.calls)
                )

        asyncio.run(run())

    def test_partial_async_round_resumes_only_missing_calls(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                blocked_id = "round-01/verify/r01-p0001/v001"
                interrupted_client = BlockingVerifierClient(blocked_id)
                interrupted = ProblemSearch(
                    problem_id="18",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=interrupted_client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                task = asyncio.create_task(interrupted.solve())
                await asyncio.wait_for(
                    interrupted_client.blocked_started.wait(), timeout=1
                )
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task

                resumed_client = ScriptedClient()
                resumed = ProblemSearch(
                    problem_id="18",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=resumed_client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )
                final = await resumed.solve()

                self.assertEqual(resumed_client.calls, [blocked_id])
                self.assertEqual(final["calls_completed"], 6)
                self.assertEqual(final["proofs_in_pool"], 2)
                self.assertTrue(
                    all(
                        len(proof.verifications) == 2
                        for proof in resumed.proofs.values()
                    )
                )

        asyncio.run(run())

    def test_complete_xml_at_length_is_admitted_without_continuation(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = CompleteXMLAtLengthClient()
                search = ProblemSearch(
                    problem_id="12",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                final = await search.solve()
                boundary = search.calls.records["round-01/generate/r01-p0000"]

                self.assertEqual(client.continuation_calls, 0)
                self.assertTrue(boundary["xml_complete_after_length"])
                self.assertEqual(final["proofs_in_pool"], 2)
                self.assertEqual(final["physical_requests_completed"], 6)

        asyncio.run(run())

    def test_length_truncated_thinking_gets_one_configured_continuation(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = LengthContinuationClient()
                search = ProblemSearch(
                    problem_id="10",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                final = await search.solve()
                forced = search.calls.records["round-01/generate/r01-p0000"]

                self.assertEqual(len(client.continuation_calls), 1)
                self.assertEqual(
                    client.continuation_calls[0]["max_new_tokens"],
                    config["solution_continuation_tokens"],
                )
                self.assertEqual(final["calls_completed"], 6)
                self.assertEqual(final["physical_requests_completed"], 7)
                self.assertEqual(forced["physical_request_count"], 2)
                self.assertEqual(
                    forced["logical_max_completion_tokens"],
                    config["max_completion_tokens"]
                    + config["solution_continuation_tokens"],
                )
                verifier_text = "\n".join(
                    message["content"]
                    for request_id, messages in client.messages.items()
                    if "/verify/" in request_id
                    for message in messages
                )
                self.assertNotIn("private unfinished reasoning", verifier_text)
                self.assertIn("Recovered proof.", verifier_text)

        asyncio.run(run())

    def test_complete_verifier_xml_at_length_avoids_continuation(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = CompleteVerifierXMLAtLengthClient()
                search = ProblemSearch(
                    problem_id="13",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                final = await search.solve()
                boundary = search.calls.records[
                    "round-01/verify/r01-p0000/v000"
                ]

                self.assertEqual(client.verifier_continuation_calls, 0)
                self.assertTrue(boundary["xml_complete_after_length"])
                self.assertEqual(boundary["verification_disposition"], "accepted")
                self.assertEqual(final["physical_requests_completed"], 6)

        asyncio.run(run())

    def test_length_truncated_verifier_gets_configured_continuation(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = LengthVerifierContinuationClient()
                search = ProblemSearch(
                    problem_id="14",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                final = await search.solve()
                forced = search.calls.records[
                    "round-01/verify/r01-p0000/v000"
                ]

                self.assertEqual(len(client.verifier_continuation_calls), 1)
                self.assertEqual(
                    client.verifier_continuation_calls[0]["max_new_tokens"],
                    config["verifier_continuation_tokens"],
                )
                self.assertEqual(forced["verification_disposition"], "accepted")
                self.assertTrue(forced["xml_valid"])
                self.assertEqual(forced["physical_request_count"], 2)
                self.assertEqual(final["physical_requests_completed"], 7)
                self.assertEqual(final["valid_verifications_completed"], 4)
                self.assertEqual(final["invalid_verifications_completed"], 0)
                analyses = [
                    verification.analysis
                    for proof in search.proofs.values()
                    for verification in proof.verifications
                ]
                self.assertNotIn("private verifier reasoning", "\n".join(analyses))

        asyncio.run(run())

    def test_invalid_forced_verifier_is_skipped_and_logged(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = LengthVerifierContinuationClient(
                    invalid_continuation=True
                )
                search = ProblemSearch(
                    problem_id="15",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                final = await search.solve()
                invalid_id = "round-01/verify/r01-p0000/v000"
                invalid = search.calls.records[invalid_id]
                summary = json.loads(
                    Path(directory, "rounds", "round-01.json").read_text()
                )

                self.assertEqual(len(client.verifier_continuation_calls), 1)
                self.assertFalse(invalid["xml_valid"])
                self.assertEqual(
                    invalid["verification_disposition"], "skipped_invalid_xml"
                )
                self.assertIn("does not match", invalid["xml_error"])
                self.assertEqual(len(search.proofs["r01-p0000"].verifications), 1)
                self.assertEqual(
                    summary["verification_stats"]["by_proof"]["r01-p0000"][
                        "invalid_sample_ids"
                    ],
                    [invalid_id],
                )
                self.assertEqual(final["valid_verifications_completed"], 3)
                self.assertEqual(final["invalid_verifications_completed"], 1)
                self.assertEqual(final["selected_proof_id"], "r01-p0001")
                self.assertEqual(final["valid_verification_count"], 2)

        asyncio.run(run())

    def test_invalid_forced_xml_is_disqualified_without_retry(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = LengthContinuationClient(invalid_continuation=True)
                search = ProblemSearch(
                    problem_id="11",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                final = await search.solve()

                self.assertEqual(len(client.continuation_calls), 1)
                self.assertEqual(final["proofs_in_pool"], 1)
                self.assertEqual(final["calls_completed"], 4)
                self.assertEqual(final["physical_requests_completed"], 5)
                self.assertFalse(
                    any("/verify/r01-p0000/" in request_id for request_id in client.calls)
                )

        asyncio.run(run())

    def test_candidates_without_xml_are_disqualified_without_replacement(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                client = MalformedCandidateClient()
                search = ProblemSearch(
                    problem_id="7",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )
                final = await search.solve()
                summary = Path(directory, "rounds", "round-01.json").read_text()

                self.assertEqual(final["proofs_in_pool"], 1)
                self.assertEqual(final["calls_completed"], 4)
                self.assertIn('"generated_proof_ids": [\n    "r01-p0001"', summary)
                self.assertFalse(
                    any("/verify/r01-p0000/" in request_id for request_id in client.calls)
                )

        asyncio.run(run())

    def test_malformed_verifier_xml_is_skipped_and_logged(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                config["verifications_per_proof"] = 3
                search = ProblemSearch(
                    problem_id="8",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=MalformedVerifierClient(),
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )
                final = await search.solve()
                summary = json.loads(
                    Path(directory, "rounds", "round-01.json").read_text()
                )

                self.assertEqual(final["valid_verifications_completed"], 4)
                self.assertEqual(final["invalid_verifications_completed"], 2)
                self.assertEqual(summary["verification_stats"]["attempted"], 6)
                self.assertEqual(summary["verification_stats"]["valid"], 4)
                self.assertEqual(summary["verification_stats"]["invalid"], 2)
                self.assertEqual(summary["best_valid_verification_count"], 2)
                for proof in search.proofs.values():
                    self.assertEqual(len(proof.verifications), 2)
                invalid = search.calls.records[
                    "round-01/verify/r01-p0000/v000"
                ]
                self.assertEqual(
                    invalid["verification_disposition"], "skipped_invalid_xml"
                )
                self.assertEqual(invalid["physical_request_count"], 1)

        asyncio.run(run())

    def test_round_fails_clearly_when_no_proof_meets_minimum_votes(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                config = small_config()
                config["max_rounds"] = 1
                search = ProblemSearch(
                    problem_id="16",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=AllMalformedVerifierClient(),
                    semaphore=asyncio.Semaphore(4),
                    config=config,
                )

                with self.assertRaisesRegex(
                    RuntimeError,
                    "no proof with at least 2 valid verifications",
                ):
                    await search.solve()
                self.assertEqual(
                    sum(
                        record["verification_disposition"]
                        == "skipped_invalid_xml"
                        for record in search.calls.records.values()
                        if "/verify/" in record["stage"]
                    ),
                    4,
                )

        asyncio.run(run())

    def test_early_stop_uses_same_engine(self):
        async def run():
            with tempfile.TemporaryDirectory() as directory:
                client = ScriptedClient(stop_after_first_round=True)
                search = ProblemSearch(
                    problem_id="6",
                    problem="Prove the claim.",
                    output_dir=Path(directory),
                    client=client,
                    semaphore=asyncio.Semaphore(4),
                    config=small_config(),
                )
                final = await search.solve()
                self.assertEqual(final["rounds_completed"], 1)
                self.assertEqual(final["proofs_in_pool"], 2)
                self.assertEqual(final["calls_completed"], 6)

        asyncio.run(run())

if __name__ == "__main__":
    unittest.main()
