"""Degenerate-loop detection for long-CoT proof/verify generations.

Faithful port of Yi-Chia Chen's original Proof-Pilot v2 detectors
(`proof_agent/v2/zlib_runaway_detector.py` + `loopguard.py`), adapted for our
harness's **blocking** completion API: we score the *finished* text post-hoc
instead of streaming. Same signals, same validated thresholds.

Why gzip (not a repetition penalty): a repetition penalty warps the sampling
distribution and corrupts legitimately-repetitive math reasoning (enumerations,
re-derivations). Aborting/rejecting a doomed generation only truncates it — it
does NOT change the distribution — so it is safe on on-policy OPD rollouts.

Two independent detectors; a text is degenerate if EITHER fires:

1. zlib runaway (primary). Signal = zlib_ratio = compressed/raw of a sliding
   12k-char window (lower = more repetitive; genuine reasoning ~0.3, loops ->0).
     - HARD: ratio < 0.05                          -> degenerate (hard token loop).
     - SOFT: ratio < 0.18 for >= 20 consecutive checks -> degenerate.
   The SOFT persistence requirement is what spares legit long math: a real
   enumeration dips below 0.18 but recovers within a few checks; a true loop
   stays sub-0.18 for 60+. Validated on OPD-32B ProofBench: 100% loop catch,
   0/1008 false positives on clean long generations.

2. loopguard local-density (backstop). A verbatim `chunk`=25-char segment
   recurring > `threshold`=8 times within a `span`=1500-char window. Calibrated:
   genuine small-case enumeration tops out ~4; real loops sit at 20+.
"""
from __future__ import annotations

import zlib
from collections import deque
from dataclasses import dataclass

# --- zlib runaway detector (Yi-Chia's validated defaults) ---
WINDOW_CHARS = 12_000
STEP_CHARS = 1_000
HARD_RATIO = 0.05
SOFT_RATIO = 0.18
SOFT_PERSIST = 20

# --- loopguard local-density backstop (Yi-Chia's validated defaults) ---
LG_CHUNK = 25
LG_STEP = 5
LG_THRESHOLD = 8
LG_SPAN = 1500


def zlib_ratio(text: str) -> float:
    """Compressed/raw size ratio. Lower = more repetitive. Empty -> 1.0."""
    b = text.encode("utf-8", "ignore")
    if not b:
        return 1.0
    return len(zlib.compress(b, 6)) / len(b)


@dataclass
class Verdict:
    abort: bool
    reason: str | None = None   # "hard" | "soft" | None
    ratio: float | None = None  # ratio at the deciding/last check
    position: int = 0           # total chars consumed when decided
    soft_run: int = 0           # consecutive sub-soft_ratio checks so far


class RunawayDetector:
    """Streaming zlib loop detector. Feed newly-decoded text via feed(); it
    evaluates the sliding window at every step boundary and, once it aborts, keeps
    returning the abort verdict. This is the primitive for real-time (streaming)
    detection; the offline zlib_runaway() below is the same logic over a whole
    string. Ported verbatim from Yi-Chia's zlib_runaway_detector.RunawayDetector."""

    def __init__(
        self,
        window_chars: int = WINDOW_CHARS,
        step_chars: int = STEP_CHARS,
        hard_ratio: float = HARD_RATIO,
        soft_ratio: float = SOFT_RATIO,
        soft_persist: int = SOFT_PERSIST,
    ) -> None:
        self.window_chars = window_chars
        self.step_chars = step_chars
        self.hard_ratio = hard_ratio
        self.soft_ratio = soft_ratio
        self.soft_persist = soft_persist
        self.reset()

    def reset(self) -> None:
        self._win: deque[str] = deque(maxlen=self.window_chars)
        self._since_check = 0
        self._total = 0
        self._soft_run = 0
        self._aborted = False
        self._last_ratio: float | None = None

    def feed(self, text: str) -> Verdict:
        if self._aborted:
            return Verdict(True, "aborted", self._last_ratio, self._total, self._soft_run)
        for ch in text or "":
            self._win.append(ch)
            self._total += 1
            self._since_check += 1
            if self._since_check >= self.step_chars and len(self._win) >= self.window_chars:
                self._since_check = 0
                v = self._check()
                if v.abort:
                    self._aborted = True
                    return v
        return Verdict(False, None, self._last_ratio, self._total, self._soft_run)

    def _check(self) -> Verdict:
        ratio = zlib_ratio("".join(self._win))
        self._last_ratio = ratio
        if ratio < self.hard_ratio:
            return Verdict(True, "hard", ratio, self._total, self._soft_run)
        if ratio < self.soft_ratio:
            self._soft_run += 1
            if self._soft_run >= self.soft_persist:
                return Verdict(True, "soft", ratio, self._total, self._soft_run)
        else:
            self._soft_run = 0
        return Verdict(False, None, ratio, self._total, self._soft_run)


def zlib_runaway(text: str, **kwargs) -> bool:
    """True if a sliding zlib window ever trips the hard tier, or the soft tier
    for `soft_persist` consecutive checks. Offline equivalent of RunawayDetector:
    feed the whole string through one detector."""
    return RunawayDetector(**kwargs).feed(text or "").abort


def _dense_first(text: str, chunk: int, step: int, threshold: int, span: int) -> int | None:
    """First offset of a chunk that recurs > `threshold` times within some
    `span`-char window (a real, local loop). None if no chunk is that locally
    dense. Ported from Yi-Chia's loopguard._dense_first."""
    t = text or ""
    if len(t) < chunk * 2:
        return None
    pos: dict[str, list[int]] = {}
    for i in range(0, len(t) - chunk, step):
        pos.setdefault(t[i:i + chunk], []).append(i)
    best: int | None = None
    for offs in pos.values():
        if len(offs) <= threshold:
            continue
        j = 0
        for k in range(len(offs)):
            while offs[k] - offs[j] > span:
                j += 1
            if k - j + 1 > threshold:
                if best is None or offs[j] < best:
                    best = offs[j]
                break
    return best


def loopguard_degenerate(
    text: str,
    *,
    chunk: int = LG_CHUNK,
    step: int = LG_STEP,
    threshold: int = LG_THRESHOLD,
    span: int = LG_SPAN,
) -> bool:
    """True only for a real local loop: one `chunk`-char segment repeated
    > `threshold` times within a `span`-char window. Scattered recurrence and
    small-case checking (spread out, or each instance differs) do NOT trip."""
    return _dense_first(text, chunk, step, threshold, span) is not None


def find_loop_cut(
    text: str,
    *,
    chunk: int = LG_CHUNK,
    step: int = LG_STEP,
    threshold: int = LG_THRESHOLD,
    span: int = LG_SPAN,
) -> int | None:
    """If `text` contains a verbatim local loop, return the index where the dense
    looping cluster begins (truncate there to keep the clean pre-loop prefix).
    Else None. Ported from Yi-Chia's loopguard.find_loop_cut."""
    return _dense_first(text, chunk, step, threshold, span)


def recent_window(text: str, window: int = 16_000) -> str:
    """The tail to scan -- a loop manifests in recently generated text, so bounding
    the scan keeps detection O(window). Ported from Yi-Chia's loopguard."""
    t = text or ""
    return t[-window:] if len(t) > window else t


def loop_onset(text: str, verdict: "Verdict | None") -> int:
    """Where to truncate a looping text to keep the clean pre-loop prefix.
    Char-precise cut for a verbatim loop; for a semantic loop (no verbatim cut)
    fall back to the zlib detector's onset estimate: the loop occupies the recent
    window + the sustained-soft run at the TAIL of this text, so cut that off.

    NB: uses len(text), not the global verdict.position. The detector is fed
    reasoning THEN content, so verdict.position counts BOTH streams; using it when
    `text` is only the reasoning (or only the content) over-subtracts and can wrongly
    clamp the onset to 0, discarding a good prefix. len(text)-relative is correct for
    whichever single stream we pass. (Derived from Yi-Chia's stream_engine._loop_onset.)"""
    t = text or ""
    cut = find_loop_cut(t)
    if cut is not None:
        return cut
    if verdict is not None:
        onset = len(t) - WINDOW_CHARS - (verdict.soft_run or 0) * STEP_CHARS
        return max(0, min(len(t), onset))
    return len(t)


def is_degenerate(text: str) -> bool:
    """A generation is degenerate if the zlib runaway detector OR the loopguard
    local-density backstop fires. Cheap (~ms) and distribution-neutral."""
    return zlib_runaway(text) or loopguard_degenerate(text)
