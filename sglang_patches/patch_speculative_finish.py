#!/usr/bin/env python3
"""Patch SGLang's multi-token finish ordering and DFlash KV-tail accounting.

A speculative verify step can publish several tokens.  Upstream currently checks
the max-token limit before EOS/stop conditions, so an earlier stop inside the
same accepted chunk can lose to a later length boundary.  The raw speculative
tail can then be emitted or inserted into the radix cache.

This patch is deliberately narrow and idempotent.  It fails closed when the
expected source shape changes instead of silently leaving a runtime unpatched.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


FINISH_MARKER = "# DFLASH_FINISH_ORDER_FIX: choose the earliest visible boundary."
FINISH_REPLAY_MARKER = "# DFLASH_FINISH_REPLAY_FIX: replay stock checks one token at a time."
KV_MARKER = "# DFLASH_FINISH_KV_FIX: rejected/post-stop tail is overallocated, not committed."
KV_HARDENED_MARKER = "# DFLASH_FINISH_KV_HARDENED: never decommit outside this verify chunk."

SCHEDULE_METHOD_RE = re.compile(
    r"    def update_finish_state\(self, new_accepted_len: int = 1\):\n"
    r".*?"
    r"(?=    def reset_for_retract\(self\):)",
    re.DOTALL,
)

LEGACY_FINISH_METHOD = '''    def update_finish_state(self, new_accepted_len: int = 1):
        if self.finished():
            return

        if self.to_finish:
            self.finished_reason = self.to_finish
            self.to_finish = None
            return

        if self.grammar is not None and self.grammar.is_terminated():
            self.finished_reason = FINISH_MATCHED_TOKEN(matched=self.output_ids[-1])
            return

        # DFLASH_FINISH_ORDER_FIX: choose the earliest visible boundary.
        # A speculative step may append more than max_new_tokens.  Hide that
        # overflow while evaluating EOS/stop conditions, then restore the raw
        # append-only buffer; output_ids_through_stop exposes only finished_len.
        raw_output_len = len(self.output_ids)
        output_len_before_step = max(0, raw_output_len - new_accepted_len)
        max_new_tokens = self.sampling_params.max_new_tokens
        visible_len = (
            raw_output_len
            if max_new_tokens is None
            else min(raw_output_len, max_new_tokens)
        )
        overflow = self.output_ids[visible_len:]
        if overflow:
            del self.output_ids[visible_len:]

        candidates = []

        def capture(checker, priority):
            self.finished_reason = None
            self.finished_len = None
            if checker():
                candidates.append(
                    (
                        self.finished_len
                        if self.finished_len is not None
                        else len(self.output_ids),
                        priority,
                        self.finished_reason,
                    )
                )

        try:
            visible_new_accepted_len = max(
                0, len(self.output_ids) - min(output_len_before_step, len(self.output_ids))
            )
            if visible_new_accepted_len > 0:
                new_accepted_tokens = self.output_ids[-visible_new_accepted_len:]
                capture(
                    lambda: self._check_token_based_finish(new_accepted_tokens),
                    0,
                )
                capture(
                    lambda: self._check_vocab_boundary_finish(new_accepted_tokens),
                    1,
                )
                capture(
                    lambda: self._check_str_based_finish(visible_new_accepted_len),
                    2,
                )

            if max_new_tokens is not None and raw_output_len >= max_new_tokens:
                candidates.append(
                    (
                        max_new_tokens,
                        3,
                        FINISH_LENGTH(length=max_new_tokens),
                    )
                )

            self.finished_reason = None
            self.finished_len = None
            if candidates:
                finished_len, _, reason = min(
                    candidates, key=lambda candidate: (candidate[0], candidate[1])
                )
                self.finished_reason = reason
                self.finished_len = finished_len
        finally:
            if overflow:
                self.output_ids.extend(overflow)

'''

NEW_FINISH_METHOD = '''    def update_finish_state(self, new_accepted_len: int = 1):
        if self.finished():
            return

        if self.to_finish:
            self.finished_reason = self.to_finish
            self.to_finish = None
            return

        # DFLASH_FINISH_ORDER_FIX: choose the earliest visible boundary.
        # DFLASH_FINISH_REPLAY_FIX: replay stock checks one token at a time.
        # Stock SGLang evaluates length, grammar, token, vocabulary, then string
        # after every generated token. A speculative verify step publishes a
        # block, so replay that exact order over the new tail. This also finds
        # the earliest match across differently ordered stop strings/regexes.
        raw_output_len = len(self.output_ids)
        output_len_before_step = max(0, raw_output_len - new_accepted_len)
        raw_tail = self.output_ids[output_len_before_step:]
        del self.output_ids[output_len_before_step:]

        try:
            for token_offset, token_id in enumerate(raw_tail, start=1):
                self.output_ids.append(token_id)

                if len(self.output_ids) >= self.sampling_params.max_new_tokens:
                    self.finished_reason = FINISH_LENGTH(
                        length=self.sampling_params.max_new_tokens
                    )
                    self.finished_len = self.sampling_params.max_new_tokens
                    return

                # Grammar state cannot be rolled back per token. DFlash rejects
                # grammar-constrained requests, while other callers retain the
                # stock whole-chunk check at the final accepted token.
                if (
                    token_offset == len(raw_tail)
                    and self.grammar is not None
                    and self.grammar.is_terminated()
                ):
                    self.finished_reason = FINISH_MATCHED_TOKEN(
                        matched=self.output_ids[-1]
                    )
                    return

                new_accepted_tokens = self.output_ids[-1:]
                if self._check_token_based_finish(new_accepted_tokens):
                    return
                if self._check_vocab_boundary_finish(new_accepted_tokens):
                    return
                if self._check_str_based_finish(1):
                    return
        finally:
            # output_ids is append-only by contract. Keep the raw speculative
            # tail for accounting; finished_len/output_ids_through_stop controls
            # what is published.
            del self.output_ids[output_len_before_step:]
            self.output_ids.extend(raw_tail)

'''

HELPER_INSERTION_POINT = "logger = logging.getLogger(__name__)\n\n\n"
KV_HELPER = '''logger = logging.getLogger(__name__)


def _trim_dflash_finished_committed_tail(req: Req, new_accepted_len: int) -> int:
    """Move unpublished DFlash KV positions from committed to overallocated."""

    if req.finished_len is None:
        return 0
    discarded = max(0, len(req.output_ids) - int(req.finished_len))
    if discarded == 0:
        return 0
    # DFLASH_FINISH_KV_HARDENED: never decommit outside this verify chunk.
    if discarded > int(new_accepted_len):
        raise RuntimeError(
            "DFLASH finished tail exceeds the current verify chunk: "
            f"{discarded=}, {new_accepted_len=}"
        )
    new_committed_len = req.kv_committed_len - discarded
    if new_committed_len < 0:
        raise RuntimeError(
            "DFLASH finished tail exceeds committed KV length: "
            f"{discarded=}, {req.kv_committed_len=}"
        )
    cache_protected_len = int(getattr(req, "cache_protected_len", 0))
    if new_committed_len < cache_protected_len:
        raise RuntimeError(
            "DFLASH finished tail would decommit protected prefix KV: "
            f"{new_committed_len=}, {cache_protected_len=}"
        )
    kv_allocated_len = int(getattr(req, "kv_allocated_len", new_committed_len))
    if new_committed_len > kv_allocated_len:
        raise RuntimeError(
            "DFLASH committed KV exceeds allocated KV after tail trim: "
            f"{new_committed_len=}, {kv_allocated_len=}"
        )
    req.kv_committed_len = new_committed_len
    return discarded


'''

LEGACY_KV_HELPER = '''logger = logging.getLogger(__name__)


def _trim_dflash_finished_committed_tail(req: Req) -> int:
    """Move unpublished DFlash KV positions from committed to overallocated."""

    if req.finished_len is None:
        return 0
    discarded = max(0, len(req.output_ids) - int(req.finished_len))
    if discarded == 0:
        return 0
    if discarded > req.kv_committed_len:
        raise RuntimeError(
            "DFLASH finished tail exceeds committed KV length: "
            f"{discarded=}, {req.kv_committed_len=}"
        )
    req.kv_committed_len -= discarded
    return discarded


'''

RESULT_CALL_OLD = '''            req.update_finish_state(new_accepted_len)

            self._handle_finish_state_updated_req(req, batch, result, i, logits_output)
'''
RESULT_CALL_NEW = '''            req.update_finish_state(new_accepted_len)

            if batch.spec_algorithm.is_dflash():
                # DFLASH_FINISH_KV_FIX: rejected/post-stop tail is overallocated, not committed.
                _trim_dflash_finished_committed_tail(req, new_accepted_len)

            self._handle_finish_state_updated_req(req, batch, result, i, logits_output)
'''

LEGACY_RESULT_CALL_NEW = '''            req.update_finish_state(new_accepted_len)

            if batch.spec_algorithm.is_dflash():
                # DFLASH_FINISH_KV_FIX: rejected/post-stop tail is overallocated, not committed.
                _trim_dflash_finished_committed_tail(req)

            self._handle_finish_state_updated_req(req, batch, result, i, logits_output)
'''


def patch_schedule_batch_text(text: str) -> str:
    if FINISH_REPLAY_MARKER in text:
        return text
    if FINISH_MARKER in text:
        patched = text.replace(LEGACY_FINISH_METHOD, NEW_FINISH_METHOD, 1)
        if patched == text:
            raise RuntimeError(
                "Could not upgrade the prior DFlash finish-order patch; "
                "the patched SGLang source layout changed."
            )
        return patched
    patched, count = SCHEDULE_METHOD_RE.subn(NEW_FINISH_METHOD, text, count=1)
    if count != 1:
        raise RuntimeError(
            "Could not locate exactly one Req.update_finish_state method; "
            "the SGLang source layout changed."
        )
    return patched


def patch_batch_result_text(text: str) -> str:
    patched = text
    if KV_MARKER in patched and KV_HARDENED_MARKER not in patched:
        if LEGACY_KV_HELPER not in patched:
            raise RuntimeError(
                "Could not upgrade the prior DFlash KV-tail helper; "
                "the patched SGLang source layout changed."
            )
        patched = patched.replace(LEGACY_KV_HELPER, KV_HELPER, 1)
        if LEGACY_RESULT_CALL_NEW not in patched:
            raise RuntimeError(
                "Could not upgrade the prior DFlash KV-tail call site."
            )
        patched = patched.replace(LEGACY_RESULT_CALL_NEW, RESULT_CALL_NEW, 1)
    if "_trim_dflash_finished_committed_tail" not in patched:
        if HELPER_INSERTION_POINT not in patched:
            raise RuntimeError("Could not locate batch_result_processor logger.")
        patched = patched.replace(HELPER_INSERTION_POINT, KV_HELPER, 1)
    if KV_MARKER not in patched:
        if RESULT_CALL_OLD not in patched:
            raise RuntimeError("Could not locate decode finish-state call site.")
        patched = patched.replace(RESULT_CALL_OLD, RESULT_CALL_NEW, 1)
    return patched


def _patch_file(path: Path, transform) -> None:
    original = path.read_text()
    patched = transform(original)
    if patched == original:
        print(f"  verified: {path.relative_to(path.parents[3])}")
        return
    backup = path.with_suffix(path.suffix + ".pre_dflash_finish_fix")
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(patched)
    print(f"  patched: {path.relative_to(path.parents[3])}")


def patch_venv(venv: Path) -> None:
    roots = list(venv.glob("lib/python*/site-packages/sglang/srt"))
    if len(roots) != 1:
        raise RuntimeError(f"Expected one sglang/srt under {venv}, found {roots}")
    root = roots[0]
    _patch_file(
        root / "managers/schedule_batch.py",
        patch_schedule_batch_text,
    )
    _patch_file(
        root / "managers/scheduler_components/batch_result_processor.py",
        patch_batch_result_text,
    )
    for pyc in (root / "managers").rglob("*.pyc"):
        pyc.unlink()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <venv_path>")
    patch_venv(Path(sys.argv[1]).resolve())
    print("[patch] speculative finish ordering and KV-tail accounting verified")


if __name__ == "__main__":
    main()
