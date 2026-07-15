from __future__ import annotations

import sys
import tomllib
import unittest
from importlib import import_module
from pathlib import Path

import torch
from transformers import AutoConfig

REPO_ROOT = Path(__file__).resolve().parents[1]
PATCH_ROOT = REPO_ROOT / "vllm_patches"
sys.path.insert(0, str(PATCH_ROOT / "src"))

plugin = import_module("olmo3_sink_vllm")
model_module = import_module("olmo3_sink_vllm.model")
dflash_module = import_module("olmo3_sink_vllm.dflash")
register = plugin.register
Olmo3SinkForCausalLM = model_module.Olmo3SinkForCausalLM
Olmo3SinkDFlashForCausalLM = dflash_module.Olmo3SinkDFlashForCausalLM
_draft_sliding_window = dflash_module._draft_sliding_window
_rope_parameters_for_layer = model_module._rope_parameters_for_layer
_select_sink_shard = model_module._select_sink_shard


class VllmOlmo3SinkPluginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = AutoConfig.from_pretrained(
            REPO_ROOT.parent / "olmo3sink-32b" / "opd-32b-deploy",
            trust_remote_code=True,
        )
        cls.draft_path = (
            REPO_ROOT.parent
            / "olmo3sink-32b"
            / "dflash-32b-draft-v2test-phaseL"
        )
        cls.draft_config = AutoConfig.from_pretrained(
            cls.draft_path,
            trust_remote_code=True,
        )

    def test_plugin_entry_point_and_registration(self) -> None:
        metadata = tomllib.loads((PATCH_ROOT / "pyproject.toml").read_text())
        entry_points = metadata["project"]["entry-points"]["vllm.general_plugins"]
        self.assertEqual(entry_points["olmo3_sink"], "olmo3_sink_vllm:register")

        from vllm import ModelRegistry

        register()
        self.assertIn("Olmo3SinkForCausalLM", ModelRegistry.get_supported_archs())
        model_class = ModelRegistry._try_load_model_cls("Olmo3SinkForCausalLM")
        self.assertIs(model_class, Olmo3SinkForCausalLM)

        for architecture in (
            "Olmo3SinkDFlashForCausalLM",
            "DFlashDraftModel",
        ):
            with self.subTest(architecture=architecture):
                self.assertIn(architecture, ModelRegistry.get_supported_archs())
                model_class = ModelRegistry._try_load_model_cls(architecture)
                self.assertIs(model_class, Olmo3SinkDFlashForCausalLM)

    def test_nested_rope_parameters_are_resolved_per_layer(self) -> None:
        full = _rope_parameters_for_layer(self.config, None)
        sliding = _rope_parameters_for_layer(self.config, self.config.sliding_window)

        self.assertEqual(full["rope_type"], "yarn")
        self.assertEqual(full["factor"], 32.0)
        self.assertEqual(full["attn_factor"], 1.3465735902799727)
        self.assertNotIn("full_attention", full)
        self.assertEqual(
            sliding,
            {"rope_type": "default", "rope_theta": 500000.0},
        )

    def test_sink_sharding_is_contiguous_by_tp_rank(self) -> None:
        weight = torch.arange(40, dtype=torch.bfloat16)
        shard = _select_sink_shard(
            weight,
            total_heads=40,
            local_heads=5,
            tp_rank=3,
        )
        torch.testing.assert_close(shard, weight[15:20])

    def test_invalid_sink_shape_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "expected 40 values"):
            _select_sink_shard(
                torch.zeros(39),
                total_heads=40,
                local_heads=5,
                tp_rank=0,
            )

    def test_target_exposes_eagle3_hidden_states(self) -> None:
        self.assertTrue(Olmo3SinkForCausalLM.supports_eagle3)
        self.assertIn(model_module.SupportsEagle3, Olmo3SinkForCausalLM.__mro__)

    def test_dflash_checkpoint_contract(self) -> None:
        from vllm.model_executor.models.qwen3_dflash import DFlashQwen3ForCausalLM

        self.assertTrue(
            issubclass(Olmo3SinkDFlashForCausalLM, DFlashQwen3ForCausalLM)
        )
        self.assertEqual(_draft_sliding_window(self.draft_config), 512)
        self.assertEqual(
            self.draft_config.dflash_config["target_layer_ids"],
            [1, 10, 18, 27, 35, 44, 52, 61],
        )
        self.assertEqual(self.draft_config.dflash_config["block_size"], 11)

    def test_dflash_checkpoint_contains_shared_model_contract(self) -> None:
        import json

        index = json.loads(
            (self.draft_path / "model.safetensors.index.json").read_text()
        )
        names = set(index["weight_map"])
        self.assertIn("mask_embed", names)
        self.assertIn("layers.0.self_attn.sinks", names)
        self.assertIn("layers.0.post_feedforward_layernorm.weight", names)
        self.assertNotIn("embed_tokens.weight", names)
        self.assertNotIn("lm_head.weight", names)


if __name__ == "__main__":
    unittest.main()
