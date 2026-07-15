"""Fail unless the configured Humming W4A8 runtime supports the visible GPU."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

import torch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--humming-path", required=True, type=Path)
    parser.add_argument("--helper-dir", required=True, type=Path)
    parser.add_argument("--nvrtc-lib", required=True, type=Path)
    args = parser.parse_args()

    package = args.humming_path / "humming" / "__init__.py"
    helper = args.helper_dir / "humming_w4a8.py"
    assert package.is_file(), package
    assert helper.is_file(), helper
    helper_source = helper.read_text()
    assert "HUMMING_SM90_FIXED_M256" in helper_source
    assert "shape_m=256" in helper_source
    assert "HUMMING_TARGET_ONLY" in helper_source
    assert 'getattr(layer, "_dflash_draft_mlp", False)' in helper_source
    assert args.nvrtc_lib.is_file(), args.nvrtc_lib
    nvrtc_builtins = args.nvrtc_lib.parent / "libnvrtc-builtins.so.13.0"
    assert nvrtc_builtins.is_file(), nvrtc_builtins

    sys.path.insert(0, str(args.humming_path))
    sys.path.insert(0, str(args.helper_dir))
    import humming
    from humming.tune import get_heuristics_class

    helper_module = importlib.import_module("humming_w4a8")
    capability = torch.cuda.get_device_capability()
    sm = capability[0] * 10 + capability[1]
    assert sm == 90, capability
    heuristic = get_heuristics_class()
    assert heuristic.__name__ == "Sm90Heuristics", heuristic.__name__

    print(
        "HUMMING_W4A8_PREFLIGHT "
        + json.dumps(
            {
                "device": torch.cuda.get_device_name(),
                "compute_capability": list(capability),
                "heuristics": heuristic.__name__,
                "humming_module": str(Path(humming.__file__).resolve()),
                "helper_module": str(Path(helper_module.__file__).resolve()),
                "humming_scope": "target_only",
                "sm90_tuning_shape_m": 256,
                "nvrtc_lib": str(args.nvrtc_lib.resolve()),
                "nvrtc_builtins": str(nvrtc_builtins.resolve()),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
