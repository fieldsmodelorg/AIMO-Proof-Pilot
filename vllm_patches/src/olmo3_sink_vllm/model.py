"""vLLM target-model implementation for Proof Pilot OLMo3Sink checkpoints."""

from __future__ import annotations

from collections.abc import Iterable
from functools import partial
from itertools import islice

import torch
from torch import nn
from transformers import Olmo3Config

from vllm.compilation.decorators import support_torch_compile
from vllm.config import VllmConfig
from vllm.distributed import get_pp_group, get_tensor_model_parallel_world_size
from vllm.distributed.communication_op import tensor_model_parallel_all_gather
from vllm.distributed.parallel_state import get_tensor_model_parallel_rank
from vllm.distributed.utils import split_tensor_along_last_dim
from vllm.logger import init_logger
from vllm.model_executor.layers.activation import SiluAndMul
from vllm.model_executor.layers.attention import Attention
from vllm.model_executor.layers.layernorm import RMSNorm
from vllm.model_executor.layers.linear import (
    MergedColumnParallelLinear,
    QKVParallelLinear,
    RowParallelLinear,
)
from vllm.model_executor.layers.logits_processor import LogitsProcessor
from vllm.model_executor.layers.rotary_embedding import get_rope
from vllm.model_executor.layers.vocab_parallel_embedding import (
    ParallelLMHead,
    VocabParallelEmbedding,
)
from vllm.model_executor.model_loader.weight_utils import default_weight_loader
from vllm.model_executor.models.interfaces import (
    EagleModelMixin,
    SupportsEagle3,
    SupportsLoRA,
    SupportsPP,
)
from vllm.model_executor.models.utils import (
    AutoWeightsLoader,
    extract_layer_index,
    is_pp_missing_parameter,
    make_empty_intermediate_tensors_factory,
    make_layers,
    maybe_prefix,
)
from vllm.sequence import IntermediateTensors

logger = init_logger(__name__)


def _normalize_rope_parameters(config: Olmo3Config, parameters: dict) -> dict:
    normalized = {
        key: value for key, value in parameters.items() if not isinstance(value, dict)
    }
    if "type" in normalized and "rope_type" not in normalized:
        normalized["rope_type"] = normalized.pop("type")
    if "attention_factor" in normalized and "attn_factor" not in normalized:
        normalized["attn_factor"] = normalized.pop("attention_factor")
    normalized.setdefault("rope_theta", getattr(config, "rope_theta", 500000))
    return normalized


def _rope_parameters_for_layer(
    config: Olmo3Config,
    sliding_window: int | None,
) -> dict:
    parameters = getattr(config, "rope_parameters", None)
    if not parameters:
        parameters = getattr(config, "rope_scaling", None) or {}
    parameters = dict(parameters)

    layer_type = "sliding_attention" if sliding_window is not None else "full_attention"
    if isinstance(parameters.get(layer_type), dict):
        parameters = dict(parameters[layer_type])
    parameters = _normalize_rope_parameters(config, parameters)

    if sliding_window is None:
        return parameters
    return {
        "rope_type": "default",
        "rope_theta": parameters["rope_theta"],
    }


def _select_sink_shard(
    weight: torch.Tensor,
    *,
    total_heads: int,
    local_heads: int,
    tp_rank: int,
) -> torch.Tensor:
    flat_weight = weight.reshape(-1)
    if flat_weight.numel() != total_heads:
        raise ValueError(
            "OLMo3Sink checkpoint has an invalid sink tensor: "
            f"expected {total_heads} values, found {flat_weight.numel()}"
        )
    start = tp_rank * local_heads
    end = start + local_heads
    if end > total_heads:
        raise ValueError(
            f"OLMo3Sink TP rank {tp_rank} requests sink heads [{start}, {end}), "
            f"but the checkpoint has only {total_heads} heads"
        )
    return flat_weight.narrow(0, start, local_heads)


class Olmo3SinkAttention(nn.Module):
    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__()
        self.config = vllm_config.model_config.hf_config
        if not isinstance(self.config, Olmo3Config):
            raise TypeError(
                "Olmo3SinkForCausalLM requires an Olmo3Config, found "
                f"{type(self.config).__name__}"
            )

        hidden_size = self.config.hidden_size
        self.tp_size = get_tensor_model_parallel_world_size()
        self.total_num_heads = self.config.num_attention_heads
        if hidden_size % self.total_num_heads != 0:
            raise ValueError("hidden_size must be divisible by num_attention_heads")
        if self.total_num_heads % self.tp_size != 0:
            raise ValueError("num_attention_heads must be divisible by TP size")

        self.num_heads = self.total_num_heads // self.tp_size
        self.total_num_kv_heads = (
            self.config.num_key_value_heads or self.total_num_heads
        )
        if self.total_num_kv_heads >= self.tp_size:
            if self.total_num_kv_heads % self.tp_size != 0:
                raise ValueError("num_key_value_heads must be divisible by TP size")
        elif self.tp_size % self.total_num_kv_heads != 0:
            raise ValueError("TP size must be divisible by num_key_value_heads")

        self.num_kv_heads = max(1, self.total_num_kv_heads // self.tp_size)
        self.head_dim = hidden_size // self.total_num_heads
        self.q_size = self.num_heads * self.head_dim
        self.kv_size = self.num_kv_heads * self.head_dim
        self.max_position_embeddings = self.config.max_position_embeddings

        attention_bias = bool(getattr(self.config, "attention_bias", False))
        self.qkv_proj = QKVParallelLinear(
            hidden_size,
            self.head_dim,
            self.total_num_heads,
            self.total_num_kv_heads,
            bias=attention_bias,
            quant_config=vllm_config.quant_config,
            prefix=f"{prefix}.qkv_proj",
        )

        self.tp_rank = get_tensor_model_parallel_rank()
        self.k_norm = RMSNorm(
            self.total_num_kv_heads * self.head_dim,
            eps=self.config.rms_norm_eps,
        )
        self.q_norm = RMSNorm(hidden_size, eps=self.config.rms_norm_eps)
        self.scaling = self.head_dim**-0.5

        layer_idx = extract_layer_index(prefix)
        layer_types = getattr(self.config, "layer_types", None)
        sliding_window = None
        if layer_types is not None and layer_types[layer_idx] == "sliding_attention":
            sliding_window = self.config.sliding_window

        sink_init_value = float(getattr(self.config, "sink_init_value", -10.0))
        self.sinks = nn.Parameter(
            torch.full((self.num_heads,), sink_init_value),
            requires_grad=False,
        )

        self.attn = Attention(
            self.num_heads,
            self.head_dim,
            self.scaling,
            num_kv_heads=self.num_kv_heads,
            cache_config=vllm_config.cache_config,
            quant_config=vllm_config.quant_config,
            per_layer_sliding_window=sliding_window,
            prefix=f"{prefix}.attn",
            sinks=self.sinks,
        )
        self.rotary_emb = get_rope(
            self.head_dim,
            max_position=self.max_position_embeddings,
            rope_parameters=_rope_parameters_for_layer(
                self.config,
                sliding_window,
            ),
        )
        self.o_proj = RowParallelLinear(
            self.total_num_heads * self.head_dim,
            hidden_size,
            bias=attention_bias,
            quant_config=vllm_config.quant_config,
            prefix=f"{prefix}.o_proj",
        )

    def _apply_qk_norm(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if self.tp_size > 1:
            query = tensor_model_parallel_all_gather(query.contiguous())
            key = tensor_model_parallel_all_gather(key.contiguous())
        query = self.q_norm(query)
        key = self.k_norm(key)
        if self.tp_size > 1:
            splitter = partial(
                split_tensor_along_last_dim,
                num_partitions=self.tp_size,
            )
            query = splitter(query)[self.tp_rank]
            key = splitter(key)[self.tp_rank]
        return query, key

    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
    ) -> torch.Tensor:
        qkv, _ = self.qkv_proj(hidden_states)
        query, key, value = qkv.split(
            [self.q_size, self.kv_size, self.kv_size],
            dim=-1,
        )
        query, key = self._apply_qk_norm(query, key)
        query, key = self.rotary_emb(positions, query, key)
        attention_output = self.attn(query, key, value)
        output, _ = self.o_proj(attention_output)
        return output


class Olmo3SinkMLP(nn.Module):
    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__()
        config = vllm_config.model_config.hf_config
        hidden_size = config.hidden_size
        intermediate_size = config.intermediate_size
        self.gate_up_proj = MergedColumnParallelLinear(
            hidden_size,
            [intermediate_size] * 2,
            bias=False,
            quant_config=vllm_config.quant_config,
            prefix=f"{prefix}.gate_up_proj",
        )
        self.act_fn = SiluAndMul()
        self.down_proj = RowParallelLinear(
            intermediate_size,
            hidden_size,
            bias=False,
            quant_config=vllm_config.quant_config,
            prefix=f"{prefix}.down_proj",
        )

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        gate_up, _ = self.gate_up_proj(hidden_states)
        hidden_states = self.act_fn(gate_up)
        hidden_states, _ = self.down_proj(hidden_states)
        return hidden_states


class Olmo3SinkDecoderLayer(nn.Module):
    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__()
        config = vllm_config.model_config.hf_config
        self.self_attn = Olmo3SinkAttention(
            vllm_config=vllm_config,
            prefix=f"{prefix}.self_attn",
        )
        self.mlp = Olmo3SinkMLP(
            vllm_config=vllm_config,
            prefix=f"{prefix}.mlp",
        )
        self.post_attention_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps,
        )
        self.post_feedforward_layernorm = RMSNorm(
            config.hidden_size,
            eps=config.rms_norm_eps,
        )

    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
    ) -> torch.Tensor:
        residual = hidden_states
        hidden_states = self.self_attn(positions, hidden_states)
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = hidden_states + residual

        residual = hidden_states
        hidden_states = self.mlp(hidden_states)
        hidden_states = self.post_feedforward_layernorm(hidden_states)
        return residual + hidden_states


@support_torch_compile(
    dynamic_arg_dims={
        "input_ids": 0,
        "positions": 0,
        "intermediate_tensors": 0,
        "inputs_embeds": 0,
    }
)
class Olmo3SinkModel(nn.Module, EagleModelMixin):
    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__()
        self.config = vllm_config.model_config.hf_config
        self.embed_tokens = VocabParallelEmbedding(
            self.config.vocab_size,
            self.config.hidden_size,
            prefix=f"{prefix}.embed_tokens",
        )
        self.start_layer, self.end_layer, self.layers = make_layers(
            self.config.num_hidden_layers,
            lambda prefix: Olmo3SinkDecoderLayer(
                vllm_config=vllm_config,
                prefix=prefix,
            ),
            prefix=f"{prefix}.layers",
        )
        self.norm = RMSNorm(
            self.config.hidden_size,
            eps=self.config.rms_norm_eps,
        )
        self.make_empty_intermediate_tensors = make_empty_intermediate_tensors_factory(
            ["hidden_states"],
            self.config.hidden_size,
        )

    def embed_input_ids(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.embed_tokens(input_ids)

    def forward(
        self,
        input_ids: torch.Tensor | None,
        positions: torch.Tensor,
        intermediate_tensors: IntermediateTensors | None,
        inputs_embeds: torch.Tensor | None = None,
    ) -> torch.Tensor | IntermediateTensors:
        if get_pp_group().is_first_rank:
            if inputs_embeds is not None:
                hidden_states = inputs_embeds
            else:
                hidden_states = self.embed_tokens(input_ids)
        else:
            if intermediate_tensors is None:
                raise ValueError("pipeline rank requires intermediate_tensors")
            hidden_states = intermediate_tensors["hidden_states"]

        aux_hidden_states = self._maybe_add_hidden_state(
            [],
            self.start_layer,
            hidden_states,
            None,
        )
        for layer_idx, layer in enumerate(
            islice(self.layers, self.start_layer, self.end_layer),
            start=self.start_layer,
        ):
            hidden_states = layer(positions, hidden_states)
            self._maybe_add_hidden_state(
                aux_hidden_states,
                layer_idx + 1,
                hidden_states,
                None,
            )

        if not get_pp_group().is_last_rank:
            return IntermediateTensors({"hidden_states": hidden_states})
        hidden_states = self.norm(hidden_states)
        if aux_hidden_states:
            return hidden_states, aux_hidden_states
        return hidden_states

    def load_weights(
        self,
        weights: Iterable[tuple[str, torch.Tensor]],
    ) -> set[str]:
        stacked_params_mapping = [
            ("qkv_proj", "q_proj", "q"),
            ("qkv_proj", "k_proj", "k"),
            ("qkv_proj", "v_proj", "v"),
            ("gate_up_proj", "gate_proj", 0),
            ("gate_up_proj", "up_proj", 1),
        ]
        params = dict(self.named_parameters(remove_duplicate=False))
        loaded_params: set[str] = set()

        for name, loaded_weight in weights:
            if is_pp_missing_parameter(name, self):
                continue
            for param_name, weight_name, shard_id in stacked_params_mapping:
                if weight_name not in name:
                    continue
                mapped_name = name.replace(weight_name, param_name)
                if mapped_name.endswith(".bias") and mapped_name not in params:
                    break
                param = params[mapped_name]
                param.weight_loader(param, loaded_weight, shard_id)
                loaded_params.add(mapped_name)
                break
            else:
                if name.endswith(".bias") and name not in params:
                    continue
                param = params[name]
                weight_loader = getattr(
                    param,
                    "weight_loader",
                    default_weight_loader,
                )
                weight_loader(param, loaded_weight)
                loaded_params.add(name)
        return loaded_params


class Olmo3SinkForCausalLM(
    nn.Module,
    SupportsPP,
    SupportsLoRA,
    SupportsEagle3,
):
    packed_modules_mapping = {
        "qkv_proj": ["q_proj", "k_proj", "v_proj"],
        "gate_up_proj": ["gate_proj", "up_proj"],
    }

    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        super().__init__()
        self.config = vllm_config.model_config.hf_config
        self.model = Olmo3SinkModel(
            vllm_config=vllm_config,
            prefix=maybe_prefix(prefix, "model"),
        )
        if self.config.tie_word_embeddings:
            self.lm_head = self.model.embed_tokens
        else:
            self.lm_head = ParallelLMHead(
                self.config.vocab_size,
                self.config.hidden_size,
                quant_config=vllm_config.quant_config,
                prefix=maybe_prefix(prefix, "lm_head"),
            )
        self.logits_processor = LogitsProcessor(self.config.vocab_size)
        self.make_empty_intermediate_tensors = (
            self.model.make_empty_intermediate_tensors
        )

    def embed_input_ids(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.model.embed_input_ids(input_ids)

    def forward(
        self,
        input_ids: torch.Tensor | None,
        positions: torch.Tensor,
        intermediate_tensors: IntermediateTensors | None = None,
        inputs_embeds: torch.Tensor | None = None,
    ) -> torch.Tensor | IntermediateTensors:
        return self.model(
            input_ids=input_ids,
            positions=positions,
            intermediate_tensors=intermediate_tensors,
            inputs_embeds=inputs_embeds,
        )

    def compute_logits(self, hidden_states: torch.Tensor) -> torch.Tensor | None:
        return self.logits_processor(self.lm_head, hidden_states)

    def load_weights(
        self,
        weights: Iterable[tuple[str, torch.Tensor]],
    ) -> set[str]:
        tp_size = get_tensor_model_parallel_world_size()
        tp_rank = get_tensor_model_parallel_rank()
        local_heads = self.config.num_attention_heads // tp_size
        params = dict(self.named_parameters(remove_duplicate=False))
        expected_sinks = {name for name in params if name.endswith(".self_attn.sinks")}
        loaded_sinks: set[str] = set()

        def without_sinks() -> Iterable[tuple[str, torch.Tensor]]:
            for name, weight in weights:
                if not name.endswith(".self_attn.sinks"):
                    yield name, weight
                    continue
                param = params.get(name)
                if param is None:
                    if is_pp_missing_parameter(name, self):
                        continue
                    raise ValueError(f"Unexpected OLMo3Sink parameter {name!r}")
                shard = _select_sink_shard(
                    weight,
                    total_heads=self.config.num_attention_heads,
                    local_heads=local_heads,
                    tp_rank=tp_rank,
                ).to(device=param.device, dtype=param.dtype)
                weight_loader = getattr(
                    param,
                    "weight_loader",
                    default_weight_loader,
                )
                weight_loader(param, shard)
                loaded_sinks.add(name)

        loader = AutoWeightsLoader(
            self,
            skip_prefixes=(
                ["lm_head.weight"] if self.config.tie_word_embeddings else None
            ),
        )
        loaded = loader.load_weights(without_sinks())
        missing_sinks = expected_sinks - loaded_sinks
        if missing_sinks:
            preview = ", ".join(sorted(missing_sinks)[:4])
            raise ValueError(
                "OLMo3Sink checkpoint did not provide every local attention sink; "
                f"missing {len(missing_sinks)} tensor(s): {preview}"
            )
        logger.info("Loaded %d OLMo3Sink attention tensors", len(loaded_sinks))
        return set(loaded) | loaded_sinks


__all__ = ["Olmo3SinkForCausalLM"]
