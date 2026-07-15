#!/usr/bin/env python3
"""Emit auditable proof whenever a Humming W4A8 layer is constructed."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


RELATIVE_PATH = Path(
    "layers/quantization/compressed_tensors/schemes/compressed_tensors_wNa16.py"
)
BUILD = "            built = hm.build_humming_w4a8(layer, self.group_size, self.symmetric)"
OLD_MARKER = (
    BUILD
    + "\n            if built:\n"
    + '                logger.info("HUMMING_W4A8_LAYER_READY device=%s group_size=%s", '\
    + "layer.weight_packed.device, self.group_size)"
)
MARKER = (
    BUILD
    + "\n            if built:\n"
    + '                logger.info("HUMMING_W4A8_LAYER_READY device=%s group_size=%s", '\
    + "layer.weight_packed.device, self.group_size)"
    + '\n            elif getattr(layer, "_dflash_draft_mlp", False):\n'
    + '                logger.info("DFLASH_DRAFT_W4A16_LAYER_READY device=%s group_size=%s", '
    + "layer.weight_packed.device, self.group_size)"
)


def patch_source(source: str) -> str:
    if MARKER not in source:
        if OLD_MARKER in source:
            source = source.replace(OLD_MARKER, MARKER, 1)
        elif source.count(BUILD) == 1:
            source = source.replace(BUILD, MARKER, 1)
        else:
            raise RuntimeError("Expected exactly one Humming build call")
    if source.count("HUMMING_W4A8_LAYER_READY") != 1:
        raise RuntimeError("Expected exactly one Humming runtime marker")
    if source.count("DFLASH_DRAFT_W4A16_LAYER_READY") != 1:
        raise RuntimeError("Expected exactly one DFlash W4A16 runtime marker")
    return source


def patch_venv(venv: Path) -> None:
    roots = list(venv.glob("lib/python*/site-packages/sglang/srt"))
    if len(roots) != 1:
        raise RuntimeError(f"Expected one sglang/srt under {venv}, found {roots}")
    path = roots[0] / RELATIVE_PATH
    original = path.read_text()
    patched = patch_source(original)
    if patched != original:
        backup = path.with_suffix(path.suffix + ".pre_w4a8_runtime_marker")
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(patched)
        print(f"  patched: {path.relative_to(roots[0])}")
    else:
        print(f"  verified: {path.relative_to(roots[0])}")
    for pyc in path.parent.glob("compressed_tensors_wNa16*.pyc"):
        pyc.unlink()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <venv_path>")
    patch_venv(Path(sys.argv[1]).resolve())
    print("[patch] W4A8 runtime marker verified")


if __name__ == "__main__":
    main()
