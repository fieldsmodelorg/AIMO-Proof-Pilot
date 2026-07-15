"""Launch the one strictly configured OPD SGLang server."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

from eval_config import active_model, load_config

REPO = Path(__file__).resolve().parents[2]


def decode_graph_batches(maximum: int) -> list[int]:
    return [
        value
        for value in [*range(1, 17), 20, 24, 28, 32, 40, 48, 64, 96, 128]
        if value <= maximum
    ]


def _prepend(env: dict[str, str], key: str, value: str) -> None:
    env[key] = f"{value}:{env[key]}" if env.get(key) else value


def attention_arguments(server: dict) -> list[str]:
    arguments = [
        "--attention-backend", str(server["attention_backend"]),
        "--page-size", str(server["page_size"]),
    ]
    if server["deterministic_inference"]:
        arguments.append("--enable-deterministic-inference")
    return arguments


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    config = load_config(args.config)
    model = active_model(config)
    server = config["server"]
    venv = Path(os.environ.get("VENV", "/workspace/pp/venv"))
    env = os.environ.copy()
    gpu_count = model.tensor_parallel_size * model.data_parallel_size
    default_gpus = ",".join(map(str, range(gpu_count)))
    env["CUDA_VISIBLE_DEVICES"] = env.get("CUDA_VISIBLE_DEVICES", default_gpus)
    if len(env["CUDA_VISIBLE_DEVICES"].split(",")) != gpu_count:
        raise RuntimeError(
            "CUDA_VISIBLE_DEVICES count must equal "
            "model.tensor_parallel_size * model.data_parallel_size"
        )

    env["FLASHINFER_CUDA_ARCH_LIST"] = env.get("FLASHINFER_CUDA_ARCH_LIST", "9.0a")
    env["FLASHINFER_USE_CUDA_NORM"] = "1"
    env["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    env["SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN"] = "1"
    env["SGLANG_ENABLE_OVERLAP_PLAN_STREAM"] = "1"
    env["SGLANG_SWA_EVICTION_INTERVAL_MULTIPLIER"] = "0.125"
    env["SGLANG_OPT_SWA_RELEASE_LEAF_LOCK_AFTER_WINDOW"] = "1"

    nvrtc_dir = venv / "lib/python3.12/site-packages/nvidia/cu13/lib"
    nvrtc_lib = nvrtc_dir / "libnvrtc.so.13"
    cuda_driver = Path("/usr/lib/x86_64-linux-gnu/libcuda.so.1")
    cuda_link_dir = Path("/tmp/pp_link")
    cccl_include = venv / "lib/python3.12/site-packages/flashinfer/data/cccl/libcudacxx/include"
    cuda_include = venv / "lib/python3.12/site-packages/nvidia/cu13/include"
    for path in (nvrtc_lib, cuda_driver, cccl_include, cuda_include):
        if not path.exists():
            raise FileNotFoundError(path)
    cuda_link_dir.mkdir(parents=True, exist_ok=True)
    libcuda_link = cuda_link_dir / "libcuda.so"
    libcuda_link.unlink(missing_ok=True)
    libcuda_link.symlink_to(cuda_driver)
    cccl_link = cuda_include / "cccl"
    cccl_link.unlink(missing_ok=True)
    cccl_link.symlink_to(cccl_include)
    _prepend(env, "LIBRARY_PATH", str(cuda_link_dir))

    if model.quantized:
        env["SGLANG_USE_HUMMING_W4A8"] = "1"
        env["W4A8_DROP_MARLIN"] = "1"
        env["W4A8_M_THRESHOLD"] = "64"
        env["W4A8_HELPER_DIR"] = env.get("W4A8_HELPER_DIR", "/workspace/pp/proof-pilot/deploy/w4a8")
        env["HUMMING_PATH"] = env.get("HUMMING_PATH", "/workspace/pp")
        _prepend(env, "LD_PRELOAD", str(nvrtc_lib))
        _prepend(env, "LD_LIBRARY_PATH", str(nvrtc_dir))
        subprocess.run(
            [
                str(venv / "bin/python"), str(REPO / "evaluation/harness/validate_humming_install.py"),
                "--humming-path", env["HUMMING_PATH"], "--helper-dir", env["W4A8_HELPER_DIR"],
                "--nvrtc-lib", str(nvrtc_lib),
            ],
            check=True, env=env,
        )
    else:
        env["SGLANG_USE_HUMMING_W4A8"] = "0"

    command = [
        str(venv / "bin/python"), "-m", "sglang.launch_server",
        "--model-path", str(model.target), *attention_arguments(server),
        "--tp", str(model.tensor_parallel_size), "--dp", str(model.data_parallel_size),
        "--load-balance-method", "round_robin", "--host", str(server["host"]),
        "--port", str(server["port"]), "--mem-fraction-static", str(server["mem_fraction_static"]),
        "--chunked-prefill-size", str(server["chunked_prefill_size"]),
        "--context-length", str(server["context_length"]), "--kv-cache-dtype", model.kv_cache_dtype,
        "--stream-interval", str(server["stream_interval"]),
        "--swa-full-tokens-ratio", str(server["swa_full_tokens_ratio"]),
        "--max-running-requests", str(server["max_running_requests"]),
        "--cuda-graph-max-bs-decode", str(server["max_running_requests"]),
        "--cuda-graph-bs-decode", *map(str, decode_graph_batches(server["max_running_requests"])),
        "--cuda-graph-backend-prefill", str(server["prefill_cuda_graph_backend"]),
        "--cuda-graph-bs-prefill", "256", "1024", str(server["chunked_prefill_size"]),
        "--enable-cache-report", "--enable-metrics", "--random-seed", str(config["search"]["seed"]),
        "--reasoning-parser", "deepseek-r1",
    ]
    if model.dflash:
        env["SGLANG_DFLASH_DRAFT_RING"] = "1"
        env["SGLANG_DFLASH_DRAFT_RING_QUOTA"] = "4"
        command.extend(
            [
                "--speculative-algorithm", "DFLASH", "--speculative-draft-model-path", str(model.draft),
                "--speculative-dflash-block-size", str(server["dflash_block_size"]),
                "--speculative-num-draft-tokens", str(server["dflash_num_draft_tokens"]),
                "--speculative-draft-window-size", str(server["dflash_window_size"]),
                "--speculative-draft-attention-backend", str(server["attention_backend"]),
            ]
        )
        if model.quantized:
            command.extend(["--speculative-draft-model-quantization", "compressed-tensors"])

    print(
        f"[proof-pilot-server] mode={model.mode} dflash={str(model.dflash).lower()} "
        f"tp={model.tensor_parallel_size} dp={model.data_parallel_size} "
        f"model={model.target} draft={model.draft} kv={model.kv_cache_dtype} "
        f"attention={server['attention_backend']} page_size={server['page_size']} "
        f"deterministic={str(server['deterministic_inference']).lower()} "
        f"port={server['port']} ctx={server['context_length']}", flush=True,
    )
    os.execvpe(command[0], command, env)


if __name__ == "__main__":
    main()
