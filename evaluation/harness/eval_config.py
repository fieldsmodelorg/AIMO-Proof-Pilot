"""Load and strictly validate a Proof Pilot runtime YAML."""

from __future__ import annotations

import math
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT_KEYS = {"schema_version", "models", "model", "server", "search"}
# Optional top-level sections: present only when the operator opts in. Kept out of
# ROOT_KEYS so existing configs stay valid without them, but validated strictly
# when supplied.
OPTIONAL_ROOT_KEYS = {"traces"}
TRACES_KEYS = {
    "enabled", "dataset_repo", "secrets_file", "interval_seconds", "private",
    "run_name",
}
MODEL_PATH_KEYS = {"bf16_target", "quantized_target", "bf16_draft", "quantized_draft"}
MODEL_KEYS = {
    "tensor_parallel_size", "data_parallel_size", "quantized", "dflash", "kv_cache_dtype",
}
SERVER_KEYS = {
    "attention_backend", "page_size", "deterministic_inference",
    "host", "port", "context_length", "mem_fraction_static", "max_running_requests",
    "swa_full_tokens_ratio", "chunked_prefill_size", "stream_interval",
    "prefill_cuda_graph_backend", "watchdog_timeout",
    "dflash_block_size", "dflash_num_draft_tokens", "dflash_window_size",
}
SEARCH_KEYS = {
    "proofs_per_round", "verifications_per_proof", "top_proofs",
    "refine_parents", "reviews_per_refine_parent", "refine_review_strategy",
    "max_rounds",
    "early_stop_threshold", "temperature", "top_p", "max_completion_tokens",
    "solution_continuation_tokens", "verifier_continuation_tokens",
    "min_valid_verifications", "verifier_sees_self_evaluation",
    "refiner_sees_self_evaluation", "lenient_parsing", "filter_degenerate",
    "stream_detect",
    "concurrency", "request_timeout_seconds", "seed",
}
# Optional search knobs: present only when the operator opts in (kept out of
# SEARCH_KEYS so existing configs stay valid without them, validated when supplied).
# llm_selector: run ycchen's final LLM select-by-id stage (majority vote over shuffled
# top candidates) instead of picking the top-ranked proof. selection_votes: # voters.
# selection_candidates: how many top-ranked proofs the selector re-ranks (the model was
# only trained to choose among a small set; keep this at ycchen's trained regime, ~4 —
# it is INTENTIONALLY decoupled from top_proofs, which sizes the refinement parent pool).
# selection_max_tokens: reasoning budget per selector ballot; a ballot that hits it is
# force-closed (</think> + <selected_id>) and continued so it still casts a vote (offline
# analog of gold's time-derived selector cap). Defaults to max_completion_tokens if absent.
# selection_continuation_tokens: budget for that forced answer after the force-close.
OPTIONAL_SEARCH_KEYS = {
    "llm_selector",
    "selection_votes",
    "selection_candidates",
    "selection_max_tokens",
    "selection_continuation_tokens",
}

@dataclass(frozen=True)
class ActiveModel:
    mode: str
    target: Path
    draft: Path | None
    tensor_parallel_size: int
    data_parallel_size: int
    kv_cache_dtype: str
    quantized: bool
    dflash: bool


def _exact_keys(value: dict[str, Any], expected: set[str], section: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{section} keys differ: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )


def _positive_int(value: Any, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def detect_gpu_count() -> int:
    """GPUs visible on this node, for ``data_parallel_size: auto``.

    ``PP_GPU_COUNT`` overrides detection (used by tests, or to pin a count
    explicitly); otherwise nvidia-smi is the source of truth for the physical
    GPUs on the node -- the same query the entrypoint's GPU gate uses.
    """
    override = os.environ.get("PP_GPU_COUNT")
    if override is not None:
        if not override.isdigit() or int(override) <= 0:
            raise ValueError(f"PP_GPU_COUNT must be a positive integer, got {override!r}")
        return int(override)
    try:
        output = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(
            "data_parallel_size=auto needs GPUs, but nvidia-smi failed "
            f"({exc}); set PP_GPU_COUNT or an explicit data_parallel_size"
        ) from exc
    count = sum(1 for line in output.splitlines() if line.strip())
    if count <= 0:
        raise ValueError("data_parallel_size=auto found no GPUs via nvidia-smi")
    return count


def _resolve_data_parallel_size(model: dict[str, Any]) -> int:
    """Concrete dp width. ``auto`` = (visible GPUs) // tensor_parallel_size."""
    tp = model["tensor_parallel_size"]
    dp = model["data_parallel_size"]
    if dp != "auto":
        return dp
    visible = detect_gpu_count()
    if visible % tp != 0:
        raise ValueError(
            f"visible GPU count {visible} is not divisible by "
            f"tensor_parallel_size {tp}; set an explicit data_parallel_size"
        )
    return visible // tp


def load_config(path: Path) -> dict[str, Any]:
    config = yaml.safe_load(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("evaluation config must be a YAML mapping")
    actual = set(config)
    missing = ROOT_KEYS - actual
    extra = actual - ROOT_KEYS - OPTIONAL_ROOT_KEYS
    if missing or extra:
        raise ValueError(
            f"root keys differ: missing={sorted(missing)}, extra={sorted(extra)}"
        )
    if config["schema_version"] != 12:
        raise ValueError("schema_version must be 12")
    for section, keys in (
        ("models", MODEL_PATH_KEYS), ("model", MODEL_KEYS), ("server", SERVER_KEYS),
    ):
        value = config[section]
        if not isinstance(value, dict):
            raise ValueError(f"{section} must be a mapping")
        _exact_keys(value, keys, section)
    # search: SEARCH_KEYS required + OPTIONAL_SEARCH_KEYS allowed but not required.
    if not isinstance(config["search"], dict):
        raise ValueError("search must be a mapping")
    actual = set(config["search"])
    missing = SEARCH_KEYS - actual
    extra = actual - SEARCH_KEYS - OPTIONAL_SEARCH_KEYS
    if missing or extra:
        raise ValueError(
            f"search keys differ: missing={sorted(missing)}, extra={sorted(extra)}"
        )

    for key, value in config["models"].items():
        if not isinstance(value, str) or not value.startswith("/"):
            raise ValueError(f"models.{key} must be an absolute path")
    model = config["model"]
    _positive_int(model["tensor_parallel_size"], "model.tensor_parallel_size")
    if model["data_parallel_size"] != "auto":
        _positive_int(model["data_parallel_size"], "model.data_parallel_size")
    if type(model["quantized"]) is not bool or type(model["dflash"]) is not bool:
        raise ValueError("model.quantized and model.dflash must be booleans")
    if not isinstance(model["kv_cache_dtype"], str) or not model["kv_cache_dtype"]:
        raise ValueError("model.kv_cache_dtype must be a nonempty string")

    server = config["server"]
    if not isinstance(server["host"], str) or not server["host"]:
        raise ValueError("server.host must be a nonempty string")
    for key in (
        "page_size", "port", "context_length", "max_running_requests", "chunked_prefill_size",
        "stream_interval", "watchdog_timeout", "dflash_block_size",
        "dflash_num_draft_tokens", "dflash_window_size",
    ):
        _positive_int(server[key], f"server.{key}")
    if server["attention_backend"] not in {"fa3", "fa4", "triton"}:
        raise ValueError("server.attention_backend must be fa3, fa4, or triton")
    if type(server["deterministic_inference"]) is not bool:
        raise ValueError("server.deterministic_inference must be a boolean")
    if server["attention_backend"] == "fa4":
        if server["page_size"] != 128:
            raise ValueError("FA4 requires server.page_size=128")
        if server["deterministic_inference"]:
            raise ValueError("FA4 does not support deterministic inference")
    elif server["attention_backend"] == "fa3":
        if server["page_size"] != 1:
            raise ValueError("FA3 requires server.page_size=1")
        # deterministic_inference is OPTIONAL on FA3. Yi-Chia's DFlash rollouts run
        # FA3 nondeterministic (deploy/dflash/run_dflash_server.sh: no
        # --enable-deterministic-inference); deterministic only adds batch-invariant
        # reproducibility at a throughput cost. DFlash stays distribution-preserving
        # either way (patch_dflash_sampling.py: the verifier is distribution-
        # preserving for temp + top-p/top-k; determinism only fixes verifier coins to
        # seed+position so batch order can't perturb output).
    else:
        # triton: the only sink-correct backend on Blackwell sm120. Supports both
        # deterministic and non-deterministic (it is in sglang's radix-deterministic
        # set), so deterministic_inference is left to the config; page_size stays 1.
        if server["page_size"] != 1:
            raise ValueError("triton requires server.page_size=1")
    if not 0 < server["mem_fraction_static"] < 1:
        raise ValueError("server.mem_fraction_static must be between 0 and 1")
    if not 0 < server["swa_full_tokens_ratio"] <= 1:
        raise ValueError("server.swa_full_tokens_ratio must be in (0, 1]")

    search = config["search"]
    for key in (
        "proofs_per_round", "verifications_per_proof", "top_proofs",
        "refine_parents", "reviews_per_refine_parent", "max_rounds",
        "max_completion_tokens", "solution_continuation_tokens",
        "verifier_continuation_tokens", "min_valid_verifications",
        "concurrency", "request_timeout_seconds",
    ):
        _positive_int(search[key], f"search.{key}")
    if search["top_proofs"] > search["proofs_per_round"]:
        raise ValueError("search.top_proofs cannot exceed search.proofs_per_round")
    # Each refine call merges refine_parents distinct parents drawn from the
    # top_proofs-sized pool, so it cannot ask for more parents than the pool holds.
    if search["refine_parents"] > search["top_proofs"]:
        raise ValueError(
            "search.refine_parents cannot exceed search.top_proofs"
        )
    if search["reviews_per_refine_parent"] > search["verifications_per_proof"]:
        raise ValueError(
            "search.reviews_per_refine_parent cannot exceed "
            "search.verifications_per_proof"
        )
    if search["min_valid_verifications"] > search["verifications_per_proof"]:
        raise ValueError(
            "search.min_valid_verifications cannot exceed "
            "search.verifications_per_proof"
        )
    if not 0 < search["early_stop_threshold"] <= 1:
        raise ValueError("search.early_stop_threshold must be in (0, 1]")
    temperature = search["temperature"]
    if (
        type(temperature) not in {int, float}
        or not math.isfinite(temperature)
        or temperature < 0
    ):
        raise ValueError("search.temperature must be a finite non-negative number")
    top_p = search["top_p"]
    if (
        type(top_p) not in {int, float}
        or not math.isfinite(top_p)
        or not 0 < top_p <= 1
    ):
        raise ValueError("search.top_p must be a finite number in (0, 1]")
    if type(search["seed"]) is not int or search["seed"] < 0:
        raise ValueError("search.seed must be a non-negative integer")
    if type(search["verifier_sees_self_evaluation"]) is not bool:
        raise ValueError("search.verifier_sees_self_evaluation must be a boolean")
    if type(search["refiner_sees_self_evaluation"]) is not bool:
        raise ValueError("search.refiner_sees_self_evaluation must be a boolean")
    if type(search["lenient_parsing"]) is not bool:
        raise ValueError("search.lenient_parsing must be a boolean")
    if type(search["filter_degenerate"]) is not bool:
        raise ValueError("search.filter_degenerate must be a boolean")
    if type(search["stream_detect"]) is not bool:
        raise ValueError("search.stream_detect must be a boolean")
    if "llm_selector" in search and type(search["llm_selector"]) is not bool:
        raise ValueError("search.llm_selector must be a boolean")
    if "selection_votes" in search:
        _positive_int(search["selection_votes"], "search.selection_votes")
    if "selection_candidates" in search:
        _positive_int(search["selection_candidates"], "search.selection_candidates")
    if "selection_max_tokens" in search:
        _positive_int(search["selection_max_tokens"], "search.selection_max_tokens")
    if "selection_continuation_tokens" in search:
        _positive_int(
            search["selection_continuation_tokens"],
            "search.selection_continuation_tokens",
        )
    if search["refine_review_strategy"] not in {"worst", "random_nonideal"}:
        raise ValueError(
            "search.refine_review_strategy must be 'worst' or 'random_nonideal'"
        )

    if "traces" in config:
        _validate_traces(config["traces"])

    return config


def _validate_traces(traces: Any) -> None:
    """Strictly validate the optional `traces` section (periodic HF upload)."""
    if not isinstance(traces, dict):
        raise ValueError("traces must be a mapping")
    _exact_keys(traces, TRACES_KEYS, "traces")
    if type(traces["enabled"]) is not bool:
        raise ValueError("traces.enabled must be a boolean")
    if type(traces["private"]) is not bool:
        raise ValueError("traces.private must be a boolean")
    _positive_int(traces["interval_seconds"], "traces.interval_seconds")
    for key in ("dataset_repo", "secrets_file", "run_name"):
        if not isinstance(traces[key], str):
            raise ValueError(f"traces.{key} must be a string")
    # run_name may be "" (meaning: derive from the active target model name).
    if traces["enabled"]:
        repo = traces["dataset_repo"].strip().strip("/")
        if repo.count("/") != 1 or not all(repo.split("/")):
            raise ValueError(
                "traces.dataset_repo must be 'owner/name' when traces.enabled"
            )
        # secrets_file is OPTIONAL: "" means use the ambient HF token
        # (HF_TOKEN env var or `hf auth login`), e.g. the node's built-in login.


def active_model(config: dict[str, Any]) -> ActiveModel:
    paths = config["models"]
    model = config["model"]
    quantized = model["quantized"]
    dflash = model["dflash"]
    target = Path(paths["quantized_target"] if quantized else paths["bf16_target"])
    draft = None
    if dflash:
        draft = Path(paths["quantized_draft"] if quantized else paths["bf16_draft"])
    return ActiveModel(
        mode="humming_w4a8" if quantized else "bf16", target=target, draft=draft,
        tensor_parallel_size=model["tensor_parallel_size"],
        data_parallel_size=_resolve_data_parallel_size(model),
        kv_cache_dtype=model["kv_cache_dtype"], quantized=quantized, dflash=dflash,
    )
