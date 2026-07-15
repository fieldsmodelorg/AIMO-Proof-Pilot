#!/usr/bin/env python3
"""Restrict Humming W4A8 construction to target-model MLP projections."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


MARKER = "# HUMMING_TARGET_ONLY: the DFlash draft remains W4A16."
ORIGINAL = (
    '    Returns True on success."""\n'
    "    wp = layer.weight_packed.data            # int32 [N, K // pack_factor]"
)
PATCHED = (
    '    Returns True on success."""\n'
    f"    {MARKER}\n"
    '    if getattr(layer, "_dflash_draft_mlp", False):\n'
    "        return False\n"
    "    wp = layer.weight_packed.data            # int32 [N, K // pack_factor]"
)


def patch_source(source: str) -> str:
    if MARKER not in source:
        if source.count(ORIGINAL) != 1:
            raise RuntimeError("Expected exactly one Humming layer build entry")
        source = source.replace(ORIGINAL, PATCHED, 1)
    if source.count(MARKER) != 1:
        raise RuntimeError("Expected exactly one target-only Humming marker")
    if source.count('_dflash_draft_mlp", False') != 1:
        raise RuntimeError("Humming draft exclusion is incomplete")
    return source


def patch_helper(path: Path) -> None:
    original = path.read_text()
    patched = patch_source(original)
    if patched != original:
        backup = path.with_suffix(path.suffix + ".pre_target_scope")
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
    print("[patch] target-only Humming scope verified")


if __name__ == "__main__":
    main()
