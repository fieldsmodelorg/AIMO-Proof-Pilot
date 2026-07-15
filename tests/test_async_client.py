from __future__ import annotations

import asyncio
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

from async_client import AsyncChatClient  # noqa: E402


class FakeTokenizer:
    def __init__(self):
        self.encoded: list[str] = []

    def apply_chat_template(self, messages, **kwargs):
        return {"input_ids": [10, 11]}

    def encode(self, text, *, add_special_tokens):
        self.encoded.append(text)
        return [20, 21, 22]


def initial_response(*, reasoning: str, content: str) -> dict:
    return {
        "message": {"content": content, "reasoning_content": reasoning},
        "finish_reason": "length",
        "prompt_tokens": 200,
        "cached_prompt_tokens": 150,
        "completion_tokens": 65536,
        "reasoning_tokens": None,
        "requested_max_completion_tokens": 65536,
        "logical_max_completion_tokens": 65536,
        "physical_request_count": 1,
        "physical_prompt_tokens": 200,
        "segments": [{"kind": "chat", "finish_reason": "length"}],
        "latency_s": 2.0,
    }


class AsyncClientTests(unittest.TestCase):
    def test_completion_budget_is_forwarded_unchanged(self):
        async def run():
            client = AsyncChatClient("http://127.0.0.1:30000/v1", "test-model")
            calls: list[tuple[str, dict]] = []

            async def post(path: str, payload: dict) -> tuple[dict, float]:
                calls.append((path, payload))
                return (
                    {
                        "choices": [
                            {
                                "message": {
                                    "content": "answer",
                                    "reasoning_content": "reasoning",
                                },
                                "finish_reason": "stop",
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 200000,
                            "completion_tokens": 1,
                        },
                    },
                    0.01,
                )

            client._post = post
            try:
                result = await client.chat_raw(
                    [{"role": "user", "content": "large prompt"}],
                    max_completion_tokens=65536,
                    temperature=1.0,
                    top_p=0.95,
                    seed=7,
                    request_id="fixed-budget",
                )
            finally:
                await client.aclose()

            self.assertEqual(len(calls), 1)
            path, payload = calls[0]
            self.assertEqual(path, "/chat/completions")
            self.assertEqual(payload["max_completion_tokens"], 65536)
            self.assertEqual(result["requested_max_completion_tokens"], 65536)
            self.assertEqual(result["logical_max_completion_tokens"], 65536)
            self.assertEqual(result["physical_request_count"], 1)

        asyncio.run(run())

    def test_thinking_only_length_uses_configured_native_continuation(self):
        async def run():
            client = AsyncChatClient("http://127.0.0.1:30000/v1", "test-model")
            tokenizer = FakeTokenizer()
            client._tokenizer = tokenizer
            native_calls: list[tuple[str, dict]] = []

            async def post_native(path: str, payload: dict) -> tuple[dict, float]:
                native_calls.append((path, payload))
                return (
                    {
                        "text": (
                            "Proof body.</solution>\n"
                            "<self_evaluation>Checked.</self_evaluation>\n"
                            "<score>1</score>"
                        ),
                        "output_ids": [30, 31],
                        "meta_info": {
                            "finish_reason": {"type": "eos_token"},
                            "prompt_tokens": 65750,
                            "completion_tokens": 2,
                            "cached_tokens": 12,
                        },
                    },
                    3.0,
                )

            client._post_native = post_native
            try:
                result = await client.continue_solution_raw(
                    initial_response(reasoning="unfinished reasoning", content=""),
                    [{"role": "user", "content": "problem"}],
                    max_new_tokens=16384,
                    temperature=1.0,
                    top_p=0.95,
                    seed=7,
                    request_id="round-01/generate/r01-p0000",
                )
            finally:
                await client.aclose()

            self.assertEqual(client.native_base_url, "http://127.0.0.1:30000")
            self.assertEqual(native_calls[0][0], "/generate")
            payload = native_calls[0][1]
            self.assertEqual(payload["sampling_params"]["max_new_tokens"], 16384)
            self.assertEqual(payload["sampling_params"]["sampling_seed"], 7)
            self.assertTrue(tokenizer.encoded[0].endswith("</think>\n\n<solution>\n"))
            self.assertNotIn("</thinking>", tokenizer.encoded[0])
            self.assertTrue(result["message"]["content"].startswith("<solution>\n"))
            self.assertEqual(result["message"]["reasoning_content"], "unfinished reasoning")
            self.assertEqual(result["logical_max_completion_tokens"], 81920)
            self.assertEqual(result["physical_request_count"], 2)
            self.assertEqual(result["physical_prompt_tokens"], 65950)
            self.assertEqual(result["finish_reason"], "stop")
            self.assertTrue(result["segments"][1]["injected_solution_tag"])

        asyncio.run(run())

    def test_partial_solution_continues_without_duplicate_solution_tag(self):
        async def run():
            client = AsyncChatClient("http://127.0.0.1:30000/v1", "test-model")
            tokenizer = FakeTokenizer()
            client._tokenizer = tokenizer

            async def post_native(path: str, payload: dict) -> tuple[dict, float]:
                return (
                    {
                        "text": (
                            " completed.</solution>\n"
                            "<self_evaluation>Checked.</self_evaluation>\n"
                            "<score>1</score>"
                        ),
                        "output_ids": [40],
                        "meta_info": {
                            "finish_reason": "stop",
                            "prompt_tokens": 100,
                        },
                    },
                    1.0,
                )

            client._post_native = post_native
            try:
                result = await client.continue_solution_raw(
                    initial_response(
                        reasoning="reasoning", content="<solution>Partial proof"
                    ),
                    [{"role": "user", "content": "problem"}],
                    max_new_tokens=2048,
                    temperature=0.8,
                    top_p=0.9,
                    seed=9,
                    request_id="partial",
                )
            finally:
                await client.aclose()

            self.assertEqual(
                tokenizer.encoded[0],
                "reasoning</think><solution>Partial proof",
            )
            self.assertEqual(
                result["message"]["content"].count("<solution>"),
                1,
            )
            self.assertFalse(result["segments"][1]["injected_solution_tag"])
            self.assertEqual(result["logical_max_completion_tokens"], 67584)

        asyncio.run(run())

    def test_thinking_only_verifier_uses_configured_native_continuation(self):
        async def run():
            client = AsyncChatClient("http://127.0.0.1:30000/v1", "test-model")
            tokenizer = FakeTokenizer()
            client._tokenizer = tokenizer
            native_calls: list[tuple[str, dict]] = []

            async def post_native(path: str, payload: dict) -> tuple[dict, float]:
                native_calls.append((path, payload))
                return (
                    {
                        "text": (
                            "The proof is valid.</evaluation>\n"
                            "<suggestions>No changes.</suggestions>\n"
                            "<score>1</score>"
                        ),
                        "output_ids": [50, 51],
                        "meta_info": {
                            "finish_reason": {"type": "eos_token"},
                            "prompt_tokens": 65800,
                            "completion_tokens": 2,
                        },
                    },
                    2.5,
                )

            client._post_native = post_native
            try:
                result = await client.continue_verification_raw(
                    initial_response(reasoning="unfinished verifier reasoning", content=""),
                    [{"role": "user", "content": "verify"}],
                    max_new_tokens=4096,
                    temperature=1.0,
                    top_p=0.95,
                    seed=11,
                    request_id="round-01/verify/r01-p0000/v000",
                )
            finally:
                await client.aclose()

            self.assertEqual(native_calls[0][0], "/generate")
            payload = native_calls[0][1]
            self.assertEqual(payload["sampling_params"]["max_new_tokens"], 4096)
            self.assertEqual(payload["sampling_params"]["sampling_seed"], 11)
            self.assertTrue(tokenizer.encoded[0].endswith("</think>\n\n<evaluation>\n"))
            self.assertNotIn("</thinking>", tokenizer.encoded[0])
            self.assertTrue(result["message"]["content"].startswith("<evaluation>\n"))
            self.assertNotIn(
                "unfinished verifier reasoning", result["message"]["content"]
            )
            self.assertEqual(result["requested_verifier_continuation_tokens"], 4096)
            self.assertEqual(result["logical_max_completion_tokens"], 69632)
            self.assertEqual(result["physical_request_count"], 2)
            self.assertTrue(
                result["segments"][1]["injected_verifier_tag"]
            )

        asyncio.run(run())

    def test_partial_verification_continues_without_duplicate_evaluation_tag(self):
        async def run():
            client = AsyncChatClient("http://127.0.0.1:30000/v1", "test-model")
            tokenizer = FakeTokenizer()
            client._tokenizer = tokenizer

            async def post_native(path: str, payload: dict) -> tuple[dict, float]:
                return (
                    {
                        "text": (
                            " valid.</evaluation>\n"
                            "<suggestions>None.</suggestions>\n"
                            "<score>1</score>"
                        ),
                        "output_ids": [60],
                        "meta_info": {"finish_reason": "stop", "prompt_tokens": 100},
                    },
                    1.0,
                )

            client._post_native = post_native
            try:
                result = await client.continue_verification_raw(
                    initial_response(
                        reasoning="reasoning",
                        content="<evaluation>The proof appears",
                    ),
                    [{"role": "user", "content": "verify"}],
                    max_new_tokens=1024,
                    temperature=1.0,
                    top_p=0.95,
                    seed=12,
                    request_id="partial-verifier",
                )
            finally:
                await client.aclose()

            self.assertEqual(
                tokenizer.encoded[0],
                "reasoning</think><evaluation>The proof appears",
            )
            self.assertEqual(
                result["message"]["content"].count("<evaluation>"),
                1,
            )
            self.assertFalse(
                result["segments"][1]["injected_verifier_tag"]
            )

        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
