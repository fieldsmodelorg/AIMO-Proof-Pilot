#!/usr/bin/env python3
"""Install one canonical near-tie rule for greedy target decoding."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "# CANONICAL_GREEDY_ARGMAX: resolve numerical near-ties by lowest token id."
OLD_CALL = "batch_next_token_ids = torch.argmax(logits, -1)"
NEW_CALL = "batch_next_token_ids = canonical_greedy_argmax(logits)"
INSERT_AFTER = "logger = logging.getLogger(__name__)\n"
HELPER = """
# CANONICAL_GREEDY_ARGMAX: resolve numerical near-ties by lowest token id.
def canonical_greedy_argmax(logits: torch.Tensor) -> torch.Tensor:
    maximum = logits.amax(dim=-1, keepdim=True)
    token_ids = torch.arange(logits.shape[-1], device=logits.device)
    candidates = torch.where(
        logits >= maximum - 1e-5,
        token_ids,
        logits.shape[-1],
    )
    return candidates.amin(dim=-1)
"""


def main() -> None:
    venv = Path(sys.argv[1])
    roots = list(venv.glob("lib/python*/site-packages/sglang/srt"))
    if len(roots) != 1:
        raise RuntimeError(f"expected one sglang/srt tree, found {len(roots)}")
    path = roots[0] / "layers" / "sampler.py"
    text = path.read_text()
    if MARKER not in text:
        if INSERT_AFTER not in text or OLD_CALL not in text:
            raise RuntimeError("sampler source does not match the required patch points")
        text = text.replace(INSERT_AFTER, INSERT_AFTER + HELPER + "\n", 1)
        text = text.replace(OLD_CALL, NEW_CALL, 1)
        path.write_text(text)
    print(f"  verified: {path.relative_to(venv)}")


if __name__ == "__main__":
    main()
