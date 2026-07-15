#!/usr/bin/env python3
"""Pin Humming SM90 W4A8 to the numerically verified M=256 configuration."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


MARKER = "# HUMMING_SM90_FIXED_M256: one verified configuration for every M."
ORIGINAL = (
    '    tc = _get_heuristics_config(meta=hl.humming_metas[""], '
    "use_f16_accum=False)"
)
PATCHED = (
    f"    {MARKER}\n"
    '    tc = _get_heuristics_config(meta=hl.humming_metas[""], '
    "shape_m=256, use_f16_accum=False)"
)


def patch_source(source: str) -> str:
    if MARKER not in source:
        if source.count(ORIGINAL) != 1:
            raise RuntimeError("Expected exactly one Humming tuning selection")
        source = source.replace(ORIGINAL, PATCHED, 1)
    if source.count(MARKER) != 1 or "shape_m=256" not in source:
        raise RuntimeError("Humming SM90 fixed configuration is incomplete")
    return source


def patch_helper(path: Path) -> None:
    original = path.read_text()
    patched = patch_source(original)
    if patched != original:
        backup = path.with_suffix(path.suffix + ".pre_sm90_fixed_m256")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(patched)
        print(f"  patched: {path}")
    else:
        print(f"  verified: {path}")
    for pyc in path.parent.glob("__pycache__/humming_w4a8*.pyc"):
        pyc.unlink()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <humming_w4a8.py>")
    path = Path(sys.argv[1]).resolve()
    assert path.name == "humming_w4a8.py"
    patch_helper(path)
    print("[patch] Humming SM90 fixed M256 configuration verified")


if __name__ == "__main__":
    main()
