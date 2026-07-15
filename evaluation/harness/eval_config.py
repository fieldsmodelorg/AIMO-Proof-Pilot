"""Load and strictly validate a Proof Pilot runtime YAML."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT_KEYS = {"schema_version", "models", "model", "server", "search"}
MODEL_PATH_KEYS = {"bf16_target", "quantized_target", "bf16_draft", "quantized_draft"}
MODEL_KEYS = {
    "tensor_parallel_size", "data_parallel_size", "quantized", "dflash", "kv_cache_dtype",
}
SERVER_KEYS = {
    "attention_backend", "page_size", "deterministic_inference",
    "host", "port", "context_length", "mem_fraction_static", "max_running_requests",
    "swa_full_tokens_ratio", "chunked_prefill_size", "stream_interval",
    "prefill_cuda_graph_backend",
    "dflash_block_size", "dflash_num_draft_tokens", "dflash_window_size",
}
SEARCH_KEYS = {
    "proofs_per_round", "verifications_per_proof", "top_proofs",
    "refinements_per_proof", "analyses_per_refinement", "max_rounds",
    "early_stop_threshold", "temperature", "top_p", "max_completion_tokens",
    "solution_continuation_tokens", "verifier_continuation_tokens",
    "min_valid_verifications",
    "concurrency", "request_timeout_seconds", "seed",
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


def load_config(path: Path) -> dict[str, Any]:
    config = yaml.safe_load(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("evaluation config must be a YAML mapping")
    _exact_keys(config, ROOT_KEYS, "root")
    if config["schema_version"] != 12:
        raise ValueError("schema_version must be 12")
    for section, keys in (
        ("models", MODEL_PATH_KEYS), ("model", MODEL_KEYS), ("server", SERVER_KEYS),
        ("search", SEARCH_KEYS),
    ):
        value = config[section]
        if not isinstance(value, dict):
            raise ValueError(f"{section} must be a mapping")
        _exact_keys(value, keys, section)

    for key, value in config["models"].items():
        if not isinstance(value, str) or not value.startswith("/"):
            raise ValueError(f"models.{key} must be an absolute path")
    model = config["model"]
    _positive_int(model["tensor_parallel_size"], "model.tensor_parallel_size")
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
        "stream_interval", "dflash_block_size",
        "dflash_num_draft_tokens", "dflash_window_size",
    ):
        _positive_int(server[key], f"server.{key}")
    if server["attention_backend"] not in {"fa3", "fa4"}:
        raise ValueError("server.attention_backend must be fa3 or fa4")
    if type(server["deterministic_inference"]) is not bool:
        raise ValueError("server.deterministic_inference must be a boolean")
    if server["attention_backend"] == "fa4":
        if server["page_size"] != 128:
            raise ValueError("FA4 requires server.page_size=128")
        if server["deterministic_inference"]:
            raise ValueError("FA4 does not support deterministic inference")
    else:
        if server["page_size"] != 1:
            raise ValueError("FA3 requires server.page_size=1")
        if not server["deterministic_inference"]:
            raise ValueError("FA3 requires deterministic inference")
    if not 0 < server["mem_fraction_static"] < 1:
        raise ValueError("server.mem_fraction_static must be between 0 and 1")
    if not 0 < server["swa_full_tokens_ratio"] <= 1:
        raise ValueError("server.swa_full_tokens_ratio must be in (0, 1]")

    search = config["search"]
    for key in (
        "proofs_per_round", "verifications_per_proof", "top_proofs",
        "refinements_per_proof", "analyses_per_refinement", "max_rounds",
        "max_completion_tokens", "solution_continuation_tokens",
        "verifier_continuation_tokens", "min_valid_verifications",
        "concurrency", "request_timeout_seconds",
    ):
        _positive_int(search[key], f"search.{key}")
    if search["top_proofs"] > search["proofs_per_round"]:
        raise ValueError("search.top_proofs cannot exceed search.proofs_per_round")
    if (
        search["top_proofs"] * search["refinements_per_proof"]
        != search["proofs_per_round"]
    ):
        raise ValueError(
            "search.top_proofs * search.refinements_per_proof must equal "
            "search.proofs_per_round"
        )
    if search["analyses_per_refinement"] != search["refinements_per_proof"]:
        raise ValueError(
            "search.analyses_per_refinement must equal "
            "search.refinements_per_proof"
        )
    if search["analyses_per_refinement"] > search["verifications_per_proof"]:
        raise ValueError(
            "search.analyses_per_refinement cannot exceed "
            "search.verifications_per_proof"
        )
    if search["min_valid_verifications"] > search["verifications_per_proof"]:
        raise ValueError(
            "search.min_valid_verifications cannot exceed "
            "search.verifications_per_proof"
        )
    if search["min_valid_verifications"] < search["analyses_per_refinement"]:
        raise ValueError(
            "search.min_valid_verifications cannot be less than "
            "search.analyses_per_refinement"
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

    return config


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
        data_parallel_size=model["data_parallel_size"],
        kv_cache_dtype=model["kv_cache_dtype"], quantized=quantized, dflash=dflash,
    )
