from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / "scripts" / "prepare_vllm_model_view.py"
SPEC = importlib.util.spec_from_file_location("prepare_vllm_model_view", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PrepareVllmModelViewTests(unittest.TestCase):
    def test_creates_zero_copy_olmo3_config_view(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            target = root / "view"
            source.mkdir()
            (source / "config.json").write_text(
                json.dumps(
                    {
                        "architectures": ["Olmo3SinkForCausalLM"],
                        "model_type": "olmo3_sink",
                    }
                ),
                encoding="utf-8",
            )
            shard = source / "model-00001-of-00001.safetensors"
            shard.write_bytes(b"weights")

            MODULE.create_view(source, target)
            MODULE.create_view(source, target)

            config = json.loads((target / "config.json").read_text())
            self.assertEqual(config["model_type"], "olmo3")
            self.assertTrue((target / shard.name).is_symlink())
            self.assertEqual((target / shard.name).resolve(), shard.resolve())
            self.assertTrue(MODULE.validate_existing_view(source.resolve(), target))

    def test_rejects_non_sink_architecture(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            (source / "config.json").write_text(
                json.dumps(
                    {
                        "architectures": ["Olmo3ForCausalLM"],
                        "model_type": "olmo3",
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Expected architecture"):
                MODULE.create_view(source, root / "view")


if __name__ == "__main__":
    unittest.main()
