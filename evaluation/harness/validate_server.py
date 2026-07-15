"""Record and strictly validate the YAML-selected OPD server."""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

from eval_config import active_model, load_config


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--server-log", required=True, type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    model = active_model(config)
    expected = config["server"]
    target_config = json.loads((model.target / "config.json").read_text())
    draft_config = (
        json.loads((model.draft / "config.json").read_text()) if model.draft else None
    )
    server = get_json(args.url.rstrip("/") + "/get_server_info")
    models = get_json(args.url.rstrip("/") + "/v1/models")
    server_log = args.server_log.read_text()
    humming_layers = server_log.count("HUMMING_W4A8_LAYER_READY")
    draft_w4a16_layers = server_log.count("DFLASH_DRAFT_W4A16_LAYER_READY")

    assert target_config["torch_dtype"] == "bfloat16"
    assert server["tp_size"] == model.tensor_parallel_size
    assert server["dp_size"] == model.data_parallel_size
    assert server["kv_cache_dtype"] == model.kv_cache_dtype
    assert server["enable_fp32_lm_head"] is False
    assert server["context_length"] == expected["context_length"]
    assert server["max_running_requests"] == expected["max_running_requests"]
    assert server["cuda_graph_max_bs_decode"] == expected["max_running_requests"]
    assert server["mem_fraction_static"] == expected["mem_fraction_static"]
    assert server["chunked_prefill_size"] == expected["chunked_prefill_size"]
    assert server["stream_interval"] == expected["stream_interval"]
    assert server["swa_full_tokens_ratio"] == expected["swa_full_tokens_ratio"]
    assert server["disable_radix_cache"] is False
    assert server["disable_overlap_schedule"] is False
    assert server["disable_cuda_graph"] is False
    assert server["enable_deterministic_inference"] is expected["deterministic_inference"]
    assert server["attention_backend"] == expected["attention_backend"]
    assert server["page_size"] == expected["page_size"]
    assert models["data"][0]["id"] == str(model.target)

    if model.quantized:
        assert target_config["quantization_config"]["quant_method"] == "compressed-tensors"
        assert "HUMMING_W4A8_PREFLIGHT " in server_log
        assert humming_layers == 128 * model.tensor_parallel_size * model.data_parallel_size, humming_layers
        assert "target_execution=humming_w4a8" in server_log
    else:
        assert target_config.get("quantization_config") is None
        assert humming_layers == 0
        assert "HUMMING_W4A8_PREFLIGHT " not in server_log

    if model.dflash:
        assert draft_config is not None
        assert draft_config["torch_dtype"] == "bfloat16"
        assert server["speculative_algorithm"] == "DFLASH"
        assert server["speculative_draft_model_path"] == str(model.draft)
        assert server["speculative_dflash_block_size"] == expected["dflash_block_size"]
        assert server["speculative_num_draft_tokens"] == expected["dflash_num_draft_tokens"]
        assert server["speculative_draft_window_size"] == expected["dflash_window_size"]
        assert server["speculative_draft_attention_backend"] == expected["attention_backend"]
        expected_ring = expected["page_size"] == 1
        assert f"draft_kv_ring={expected_ring}" in server_log
        if expected_ring:
            assert "DFLASH draft KV ring:" in server_log
        else:
            assert "DFLASH draft KV ring" not in server_log
        if model.quantized:
            assert draft_config["quantization_config"]["quant_method"] == "compressed-tensors"
            assert server["speculative_draft_model_quantization"] == "compressed-tensors"
            assert draft_w4a16_layers == 16 * model.tensor_parallel_size * model.data_parallel_size
        else:
            assert draft_config.get("quantization_config") is None
            assert server["speculative_draft_model_quantization"] is None
            assert draft_w4a16_layers == 0
    else:
        assert draft_config is None
        assert server["speculative_algorithm"] is None
        assert server["speculative_draft_model_path"] is None
        assert server["speculative_draft_model_quantization"] is None
        assert draft_w4a16_layers == 0
        assert "DFLASH draft KV ring" not in server_log

    result = {
        "schema_version": 2,
        "evaluation_config": config,
        "active_model": {
            "mode": model.mode,
            "target": str(model.target),
            "draft": str(model.draft) if model.draft else None,
            "tensor_parallel_size": model.tensor_parallel_size,
            "data_parallel_size": model.data_parallel_size,
            "quantized": model.quantized,
            "dflash": model.dflash,
        },
        "server": server,
        "models": models,
        "target_config": target_config,
        "draft_config": draft_config,
        "gpus": subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total,memory.free",
                "--format=csv,noheader,nounits",
            ],
            text=True,
        ).splitlines(),
        "runtime_markers": {
            "humming_preflight": "HUMMING_W4A8_PREFLIGHT " in server_log,
            "humming_target_layer_count": humming_layers,
            "dflash_draft_w4a16_layer_count": draft_w4a16_layers,
            "dflash_ring": "DFLASH draft KV ring" in server_log,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
