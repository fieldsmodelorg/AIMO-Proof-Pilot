#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import socket
from pathlib import Path


EXPECTED_VLLM_VERSION = "0.25.1"


def main() -> None:
    import vllm
    from vllm import ModelRegistry
    from vllm.plugins import load_general_plugins

    if vllm.__version__ != EXPECTED_VLLM_VERSION:
        raise RuntimeError(
            f"Expected vLLM {EXPECTED_VLLM_VERSION}, got {vllm.__version__} "
            f"from {vllm.__file__}"
        )

    load_general_plugins()
    required_architectures = {
        "Olmo3SinkForCausalLM",
        "Olmo3SinkDFlashForCausalLM",
        "DFlashDraftModel",
    }
    missing = required_architectures - set(ModelRegistry.get_supported_archs())
    if missing:
        raise RuntimeError(f"Missing vLLM plugin architectures: {sorted(missing)}")

    from evaluation.harness_vllm import run

    runtime = run.DistributedRuntime.from_environment()
    metadata = {
        "smoke": "nii-vllm-0.25.1-controller",
        "vllm_version": vllm.__version__,
        "repo_commit": os.environ.get("NII_INFERENCE_REPO_COMMIT", "unknown"),
    }
    runtime.initialize(metadata)
    runtime.synchronize_stage("controller-smoke")

    result = {
        "status": "ok",
        "rank": runtime.rank,
        "world_size": runtime.world_size,
        "hostname": socket.gethostname(),
        "run_id": runtime.run_id,
        "session_dir": str(runtime.session_dir),
        "vllm_version": vllm.__version__,
        "vllm_file": str(Path(vllm.__file__).resolve()),
        "assigned_candidates_for_14": runtime.assigned_attempt_indices(14),
    }
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
