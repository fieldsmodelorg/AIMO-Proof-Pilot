from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "evaluation" / "harness"
sys.path.insert(0, str(HARNESS))

from loop_detect import (  # noqa: E402
    Verdict,
    find_loop_cut,
    is_degenerate,
    loop_onset,
    loopguard_degenerate,
    recent_window,
    zlib_ratio,
    zlib_runaway,
)


def _high_entropy_reasoning(n_lines: int) -> str:
    """Long, genuinely non-repetitive text: each line carries two unique hashes,
    so LZ77 can't collapse it -- stands in for real varied reasoning."""
    out = []
    for i in range(n_lines):
        a = hashlib.md5(f"a{i}".encode()).hexdigest()
        b = hashlib.md5(f"b{i}".encode()).hexdigest()
        out.append(
            f"Step {i}: consider the case {a}; it forces {b} so the bound {i * i % 997} holds."
        )
    return "\n".join(out)


class ZlibRatioTest(unittest.TestCase):
    def test_empty_is_one(self) -> None:
        self.assertEqual(zlib_ratio(""), 1.0)

    def test_loop_ratio_far_below_varied_text(self) -> None:
        loop = "1, " * 4000
        varied = _high_entropy_reasoning(3000)
        self.assertLess(zlib_ratio(loop), 0.05)        # hard-loop territory
        self.assertGreater(zlib_ratio(varied), 0.18)   # genuine reasoning stays high


class DetectorTest(unittest.TestCase):
    def test_pure_token_loop_is_degenerate(self) -> None:
        text = "1, " * 6000  # classic "1,1,1,..." runaway
        self.assertTrue(zlib_runaway(text))
        self.assertTrue(is_degenerate(text))

    def test_repeated_verbatim_chunk_trips_loopguard(self) -> None:
        # 15-char period (aligns with the 5-char step) repeated densely.
        text = "the loop line.\n" * 500
        self.assertTrue(loopguard_degenerate(text))
        self.assertTrue(is_degenerate(text))

    def test_clean_varied_reasoning_not_degenerate(self) -> None:
        text = _high_entropy_reasoning(4000)
        self.assertGreater(len(text), 12_000)
        self.assertFalse(zlib_runaway(text))
        self.assertFalse(loopguard_degenerate(text))
        self.assertFalse(is_degenerate(text))

    def test_short_text_is_never_degenerate(self) -> None:
        self.assertFalse(is_degenerate("a short proof."))
        self.assertFalse(is_degenerate(""))


class SalvageHelperTests(unittest.TestCase):
    def test_loop_onset_is_length_relative_and_clamps(self):
        # short text + large soft_run: onset goes negative -> clamp to 0 (no crash, and
        # NOT driven by a global position that over-subtracts). Regression for audit #1.
        self.assertEqual(loop_onset("short clean prefix", Verdict(True, "soft", 0.07, 99999, 20)), 0)
        # long high-entropy text (no verbatim loop): onset = len - WINDOW - soft_run*STEP
        text = "".join(hashlib.md5(str(i).encode()).hexdigest() for i in range(2000))
        v = Verdict(True, "soft", 0.07, len(text) + 500, 5)
        self.assertEqual(loop_onset(text, v), max(0, len(text) - 12000 - 5 * 1000))
        # verbatim loop -> returns the find_loop_cut onset regardless of the verdict
        loopy = "clean start here. " + "the loop line.\n" * 500
        self.assertEqual(loop_onset(loopy, v), find_loop_cut(loopy))
        # no verdict -> keep everything
        self.assertEqual(loop_onset("abc", None), 3)

    def test_find_loop_cut_and_recent_window(self):
        self.assertIsNone(find_loop_cut("a short clean sentence with no loop."))
        cut = find_loop_cut("prefix here. " + "the loop line.\n" * 500)
        self.assertIsNotNone(cut)
        self.assertLess(cut, 80)  # cut sits near the clean-prefix boundary
        self.assertEqual(len(recent_window("x" * 20000, window=16000)), 16000)
        self.assertEqual(recent_window("short", window=16000), "short")


if __name__ == "__main__":
    unittest.main()
