from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

import loop_detect  # noqa: E402
from async_client import AsyncChatClient  # noqa: E402


def _sse(chunks: list[tuple]) -> list[str]:
    """Build OpenAI-style SSE `data:` lines from (reasoning, content, finish, usage)."""
    lines = []
    for reasoning, content, finish, usage in chunks:
        delta = {}
        if reasoning is not None:
            delta["reasoning_content"] = reasoning
        if content is not None:
            delta["content"] = content
        obj = {"choices": [{"delta": delta, "finish_reason": finish}]}
        if usage is not None:
            obj["usage"] = usage
        lines.append("data: " + json.dumps(obj))
    lines.append("data: [DONE]")
    return lines


async def _aiter(lines):
    for line in lines:
        yield line


def _run(coro):
    return asyncio.run(coro)


class ConsumeSseTests(unittest.TestCase):
    def _client(self):
        return AsyncChatClient(base_url="http://localhost:0/v1", model="m")

    def test_clean_stream_completes_without_abort(self):
        client = self._client()
        try:
            lines = _sse([
                ("Let us reason step by step about the claim. ", None, None, None),
                (None, "<solution>The proof body.</solution>\n<score>1</score>", "stop",
                 {"prompt_tokens": 5, "completion_tokens": 20}),
            ])
            state = _run(client._consume_sse(_aiter(lines), loop_detect.RunawayDetector()))
        finally:
            _run(client.aclose())
        self.assertFalse(state["aborted"])
        self.assertEqual(state["finish_reason"], "stop")
        self.assertIn("<solution>", state["content"])
        self.assertEqual(state["usage"]["completion_tokens"], 20)

    def test_looping_stream_aborts(self):
        client = self._client()
        try:
            # a hard token loop streamed across many chunks (well past the 12k window)
            lines = _sse([("1, " * 500, None, None, None) for _ in range(40)])
            state = _run(client._consume_sse(_aiter(lines), loop_detect.RunawayDetector()))
        finally:
            _run(client.aclose())
        self.assertTrue(state["aborted"])
        self.assertIsNotNone(state["verdict"])
        self.assertTrue(state["verdict"].abort)


class SalvageStreamTests(unittest.TestCase):
    def _client(self):
        return AsyncChatClient(base_url="http://localhost:0/v1", model="m")

    def _record(self, content, reasoning):
        return {
            "message": {"content": content, "reasoning_content": reasoning},
            "finish_reason": "length",
            "requested_max_completion_tokens": 128,
            "segments": [],
            "salvaged": False,
            "stop_reason": "loop",
            "stream_aborted": True,
        }

    def _mock_forceclose(self, client, recovered):
        seen = {}

        async def fake_continue(initial, messages, **kwargs):
            seen["content"] = initial["message"]["content"]
            seen["reasoning"] = initial["message"]["reasoning_content"]
            return {
                **initial,
                "message": {"content": recovered, "reasoning_content": seen["reasoning"]},
                "finish_reason": "length",
                "physical_request_count": 2,
            }

        client._continue_xml_raw = fake_continue  # avoid tokenizer / /generate
        return seen

    def test_verbatim_content_loop_forcecloses_from_clean_prefix(self):
        # A VERBATIM content loop: keep the clean <solution> prefix and FORCE-CLOSE it
        # to completion (a bare truncation lacks <score> and would fail to parse).
        client = self._client()
        clean = "<solution>Real proof step one holds. Real step two holds.\n"
        content = clean + "loop loop loop loop loop " * 400  # 25-char verbatim period
        verdict = loop_detect.RunawayDetector().feed(content)
        recovered = "<solution>Real proof done.\n</solution>\n<self_evaluation>ok</self_evaluation>\n<score>1</score>"
        seen = self._mock_forceclose(client, recovered)
        record = self._record(content, "clean reasoning")
        try:
            out = _run(client._salvage_stream_loop(
                record, [{"role": "user", "content": "x"}], "clean reasoning", content, verdict,
                role="solution", salvage_max_tokens=64, temperature=1.0, top_p=1.0, seed=0, request_id="r01",
            ))
        finally:
            _run(client.aclose())
        # force-close seeded with the clean <solution> prefix, looping tail truncated
        self.assertIn("<solution>", seen["content"].lower())
        self.assertIn("Real proof step one", seen["content"])
        self.assertLess(len(seen["content"]), len(content))
        self.assertTrue(out["salvaged"])
        self.assertEqual(out["stop_reason"], "loop")

    def test_semantic_content_loop_keeps_prefix_not_discarded(self):
        # Audit #1: a NON-verbatim (zlib) content loop (find_loop_cut == None) must keep
        # the clean <solution> prefix via loop_onset and force-close from IT -- not
        # discard the good proof and force-close from empty reasoning.
        client = self._client()
        body = "".join(
            f"Step {i} ({hashlib.md5(str(i).encode()).hexdigest()[:10]}): bound {i * i % 97}. "
            for i in range(3000)
        )
        content = "<solution>" + body
        self.assertIsNone(loop_detect.find_loop_cut(content))  # no verbatim cluster
        # simulate a zlib SOFT abort mid-content (position counts reasoning+content)
        verdict = loop_detect.Verdict(True, "soft", 0.07, len(content) + 84, 20)
        recovered = "<solution>Recovered proof.\n</solution>\n<self_evaluation>ok</self_evaluation>\n<score>1</score>"
        seen = self._mock_forceclose(client, recovered)
        record = self._record(content, "short clean reasoning")
        try:
            out = _run(client._salvage_stream_loop(
                record, [{"role": "user", "content": "x"}], "short clean reasoning", content, verdict,
                role="solution", salvage_max_tokens=64, temperature=1.0, top_p=1.0, seed=0, request_id="r02",
            ))
        finally:
            _run(client.aclose())
        # KEY: the force-close was seeded from the CLEAN CONTENT PREFIX (not empty), keeping the proof
        self.assertIn("<solution>", seen["content"].lower())
        self.assertIn("Step 0", seen["content"])
        self.assertGreater(len(seen["content"]), 1000)  # substantial prefix kept, not discarded
        self.assertTrue(out["salvaged"])

    def test_loop_in_reasoning_forcecloses_from_clean_prefix(self):
        client = self._client()
        reasoning = "GENUINE clean reasoning prefix establishing the setup. " + (
            "spin spin spin spin spin " * 300
        )
        # a genuinely varied (non-degenerate) recovered proof, > 500 chars
        recovered_body = (
            "<solution>Recovered proof. "
            + " ".join(
                f"Case {i}: as {i} is {'even' if i % 2 == 0 else 'odd'}, the bound {i * i - i + 1} holds."
                for i in range(30)
            )
            + "</solution>"
        )
        seen = {}

        async def fake_continue(initial, messages, **kwargs):
            seen["reasoning"] = initial["message"]["reasoning_content"]
            seen["role"] = kwargs.get("role")
            return {
                **initial,
                "message": {"content": recovered_body, "reasoning_content": seen["reasoning"]},
                "finish_reason": "length",
                "physical_request_count": 2,
            }

        client._continue_xml_raw = fake_continue  # avoid the tokenizer / /generate call
        verdict = loop_detect.RunawayDetector().feed(reasoning)
        record = self._record("", reasoning)
        try:
            out = _run(client._salvage_stream_loop(
                record, [{"role": "user", "content": "prove it"}], reasoning, "", verdict,
                role="solution", salvage_max_tokens=64,
                temperature=1.0, top_p=1.0, seed=0, request_id="r02",
            ))
        finally:
            _run(client.aclose())
        # force-close was invoked with a truncated (clean) reasoning, not the loop
        self.assertIn("GENUINE", seen["reasoning"])
        self.assertLess(len(seen["reasoning"]), len(reasoning))
        self.assertEqual(seen["role"], "solution")
        # a usable recovered <solution> is marked salvaged + stop
        self.assertTrue(out["salvaged"])
        self.assertEqual(out["stop_reason"], "loop")
        self.assertEqual(out["finish_reason"], "stop")
        self.assertIn("Recovered proof", out["message"]["content"])


def _gen_record() -> dict:
    return {
        "message": {
            "content": "<solution>Proof.</solution>\n"
            "<self_evaluation>ok</self_evaluation>\n<score>1</score>",
            "reasoning_content": "clean",
        },
        "finish_reason": "stop",
        "prompt_tokens": 5,
        "cached_prompt_tokens": 4,
        "completion_tokens": 10,
        "reasoning_tokens": 2,
        "requested_max_completion_tokens": 128,
        "logical_max_completion_tokens": 128,
        "physical_request_count": 1,
        "physical_prompt_tokens": 5,
        "segments": [],
        "latency_s": 0.01,
    }


class _RoutingStub:
    def __init__(self):
        self.raw = 0
        self.stream = 0

    async def chat_raw(self, messages, **kwargs):
        self.raw += 1
        return _gen_record()

    async def chat_stream(self, messages, *, role, salvage_max_tokens, **kwargs):
        self.stream += 1
        return _gen_record()


class PerformRoutingTests(unittest.TestCase):
    def _perform(self, *, stream_detect):
        from proof_search import CallSpec, CallStore  # noqa: E402
        import tempfile

        stub = _RoutingStub()
        with tempfile.TemporaryDirectory() as directory:
            store = CallStore(Path(directory))
            spec = CallSpec(
                sample_id="round-01/generate/r01-p0000",
                stage="round-01/generate",
                messages=[{"role": "user", "content": "prove it"}],
                seed=0,
            )
            _run(store.perform(
                stub, asyncio.Semaphore(1), 128, 64, 64, 1.0, 1.0, spec,
                lenient=True, stream_detect=stream_detect,
            ))
        return stub

    def test_routes_to_chat_stream_when_enabled(self):
        stub = self._perform(stream_detect=True)
        self.assertEqual((stub.stream, stub.raw), (1, 0))

    def test_routes_to_chat_raw_when_disabled(self):
        stub = self._perform(stream_detect=False)
        self.assertEqual((stub.stream, stub.raw), (0, 1))


if __name__ == "__main__":
    unittest.main()
