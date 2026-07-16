#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path


MARKER_NAME = "VLLM_MODEL_VIEW.json"
EXPECTED_ARCHITECTURE = "Olmo3SinkForCausalLM"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def validate_existing_view(source: Path, target: Path) -> bool:
    marker_path = target / MARKER_NAME
    config_path = target / "config.json"
    if not marker_path.is_file() or not config_path.is_file():
        return False
    marker = load_json(marker_path)
    config = load_json(config_path)
    return (
        Path(marker.get("source", "")) == source
        and marker.get("original_model_type") == "olmo3_sink"
        and config.get("model_type") == "olmo3"
        and EXPECTED_ARCHITECTURE in config.get("architectures", [])
    )


def create_view(source: Path, target: Path, *, force: bool = False) -> None:
    source = source.resolve()
    target = target.absolute()
    if not source.is_dir():
        raise FileNotFoundError(f"Model directory does not exist: {source}")
    if source == target:
        raise ValueError("Source and target model directories must differ")

    source_config_path = source / "config.json"
    if not source_config_path.is_file():
        raise FileNotFoundError(f"Missing model config: {source_config_path}")
    source_config = load_json(source_config_path)
    architectures = source_config.get("architectures", [])
    if EXPECTED_ARCHITECTURE not in architectures:
        raise ValueError(
            f"Expected architecture {EXPECTED_ARCHITECTURE!r}, got {architectures!r}"
        )
    original_model_type = source_config.get("model_type")
    if original_model_type not in {"olmo3", "olmo3_sink"}:
        raise ValueError(
            f"Expected model_type 'olmo3_sink' or 'olmo3', got "
            f"{original_model_type!r}"
        )

    if target.exists():
        if validate_existing_view(source, target):
            print(f"[model-view] already ready: {target}")
            return
        if not force:
            raise FileExistsError(
                f"Target exists but is not a matching model view: {target}; "
                "pass --force to replace it"
            )
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{target.name}.tmp-", dir=target.parent)
    )
    try:
        for item in source.iterdir():
            if item.name == "config.json":
                continue
            os.symlink(item, temporary / item.name, target_is_directory=item.is_dir())

        compatible_config = dict(source_config)
        compatible_config["model_type"] = "olmo3"
        (temporary / "config.json").write_text(
            json.dumps(compatible_config, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (temporary / MARKER_NAME).write_text(
            json.dumps(
                {
                    "source": str(source),
                    "original_model_type": original_model_type,
                    "view_model_type": "olmo3",
                    "architecture": EXPECTED_ARCHITECTURE,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(target)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    print(f"[model-view] ready: source={source} target={target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a zero-copy Transformers-compatible OLMo3Sink view."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_view(args.source, args.target, force=args.force)


if __name__ == "__main__":
    main()
