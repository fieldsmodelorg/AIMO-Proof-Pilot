"""vLLM DFlash draft implementation for Proof Pilot OLMo3Sink checkpoints."""

from __future__ import annotations

from collections.abc import Iterable

import torch
from torch import nn

from vllm.compilation.decorators import support_torch_compile
from vllm.config import CacheConfig, VllmConfig, get_current_vllm_config
from vllm.distributed import (
    get_tensor_model_parallel_rank,
    get_tensor_model_parallel_world_size,
)
from vllm.distributed.communication_op import tensor_model_parallel_all_gather
from vllm.distributed.utils import split_tensor_along_last_dim
from vllm.logger import init_logger
from vllm.model_executor.layers.activation import SiluAndMul
from vllm.model_executor.layers.attention import Attention
from vllm.model_executor.layers.layernorm import RMSNorm
from vllm.model_executor.layers.linear import (
    MergedColumnParallelLinear,
    QKVParallelLinear,
    ReplicatedLinear,
    RowParallelLinear,
)
from vllm.model_executor.layers.logits_processor import LogitsProcessor
from vllm.model_executor.layers.quantization.base_config import QuantizationConfig
from vllm.model_executor.layers.rotary_embedding import get_rope
from vllm.model_executor.layers.vocab_parallel_embedding import (
    ParallelLMHead,
    VocabParallelEmbedding,
)
from vllm.model_executor.model_loader.weight_utils import default_weight_loader
from vllm.model_executor.models.qwen3_dflash import (
    DFlashQwen3ForCausalLM,
    DFlashQwen3Model,
)
from vllm.model_executor.models.utils import get_draft_quant_config, maybe_prefix
from vllm.multimodal.inputs import NestedTensors
from vllm.v1.attention.backend import AttentionType

from .model import _normalize_rope_parameters, _select_sink_shard

logger = init_logger(__name__)


def _draft_config(vllm_config: VllmConfig):
    speculative_config = vllm_config.speculative_config
    if speculative_config is None or speculative_config.draft_model_config is None:
        raise ValueError("OLMo3Sink DFlash requires a draft_model_config")
    return speculative_config.draft_model_config.hf_config


def _draft_options(config) -> dict:
    options = dict(getattr(config, "eagle_config", None) or {})
    options.update(getattr(config, "dflash_config", None) or {})
    return options


def _draft_sliding_window(config) -> int:
    sliding_window = getattr(config, "sliding_window", None)
    if sliding_window is None:
        sliding_window = _draft_options(config).get("sliding_window")
    if sliding_window is None:
        raise ValueError(
            "OLMo3Sink DFlash requires sliding_window in config.json or "
            "dflash_config"
        )
    sliding_window = int(sliding_window)
    if sliding_window <= 0:
        raise ValueError("OLMo3Sink DFlash sliding_window must be positive")
    return sliding_window


def _draft_rope_parameters(config) -> dict:
    parameters = getattr(config, "rope_parameters", None)
    if not parameters:
        parameters = getattr(config, "rope_scaling", None) or {}
    parameters = _normalize_rope_parameters(config, dict(parameters))
    return {
        "rope_type": "default",
        "rope_theta": parameters.get(
            "rope_theta",
            getattr(config, "rope_theta", 500000.0),
        ),
    }


def _full_projection_norm(
    tensor: torch.Tensor,
    norm: RMSNorm,
    *,
    total_heads: int,
    local_heads: int,
    head_dim: int,
    tp_size: int,
    tp_rank: int,
) -> torch.Tensor:
    """Apply an OLMo3 Q/K norm over the global projection dimension."""
    if tp_size == 1:
        return norm(tensor)

    gathered = tensor_model_parallel_all_gather(tensor.contiguous())
    if tp_size <= total_heads:
        normalized = norm(gathered)
        return split_tensor_along_last_dim(normalized, tp_size)[tp_rank]

    replicas = tp_size // total_heads
    if total_heads * replicas != tp_size or local_heads != 1:
        raise ValueError(
            "Unsupported OLMo3Sink DFlash KV-head replication: "
            f"heads={total_heads}, local_heads={local_heads}, TP={tp_size}"
        )
    shape = gathered.shape[:-1]
    unique = gathered.view(*shape, tp_size, head_dim)[..., ::replicas, :]
    normalized = norm(unique.reshape(*shape, total_heads * head_dim))
    head_idx = tp_rank // replicas
    return normalized.view(*shape, total_heads, head_dim)[..., head_idx, :]


class Olmo3SinkDFlashAttention(nn.Module):
    """OLMo3 sink attention used by each parallel DFlash draft layer."""

    def __init__(
        self,
        *,
        config,
        cache_config: CacheConfig | None,
        quant_config: QuantizationConfig | None,
        prefix: str,
    ) -> None:
        super().__init__()
        self.config = config
        self.tp_size = get_tensor_model_parallel_world_size()
        self.tp_rank = get_tensor_model_parallel_rank()
        self.total_num_heads = int(config.num_attention_heads)
        self.total_num_kv_heads = int(
            getattr(config, "num_key_value_heads", self.total_num_heads)
            or self.total_num_heads
        )
        if self.total_num_heads % self.tp_size != 0:
            raise ValueError("DFlash num_attention_heads must be divisible by TP size")
        if self.total_num_kv_heads >= self.tp_size:
            if self.total_num_kv_heads % self.tp_size != 0:
                raise ValueError("DFlash num_key_value_heads must be divisible by TP size")
        elif self.tp_size % self.total_num_kv_heads != 0:
            raise ValueError("DFlash TP size must be divisible by num_key_value_heads")

        hidden_size = int(config.hidden_size)
        self.num_heads = self.total_num_heads // self.tp_size
        self.num_kv_heads = max(1, self.total_num_kv_heads // self.tp_size)
        self.head_dim = int(
            getattr(config, "head_dim", None)
            or hidden_size // self.total_num_heads
        )
        self.q_size = self.num_heads * self.head_dim
        self.kv_size = self.num_kv_heads * self.head_dim
        attention_bias = bool(getattr(config, "attention_bias", False))

        self.qkv_proj = QKVParallelLinear(
            hidden_size,
            self.head_dim,
            self.total_num_heads,
            self.total_num_kv_heads,
            bias=attention_bias,
            quant_config=quant_config,
            prefix=f"{prefix}.qkv_proj",
        )
        self.o_proj = RowParallelLinear(
            self.total_num_heads * self.head_dim,
            hidden_size,
            bias=attention_bias,
            quant_config=quant_config,
            prefix=f"{prefix}.o_proj",
        )
        self.q_norm = RMSNorm(
            self.total_num_heads * self.head_dim,
            eps=float(config.rms_norm_eps),
        )
        self.k_norm = RMSNorm(
            self.total_num_kv_heads * self.head_dim,
            eps=float(config.rms_norm_eps),
        )
        self.rotary_emb = get_rope(
            self.head_dim,
            max_position=int(config.max_position_embeddings),
            rope_parameters=_draft_rope_parameters(config),
        )
        self.sliding_window = _draft_sliding_window(config)
        sink_init_value = float(getattr(config, "sink_init_value", -10.0))
        self.sinks = nn.Parameter(
            torch.full((self.num_heads,), sink_init_value),
            requires_grad=False,
        )
        self.attn = Attention(
            self.num_heads,
            self.head_dim,
            self.head_dim**-0.5,
            num_kv_heads=self.num_kv_heads,
            cache_config=cache_config,
            quant_config=quant_config,
            per_layer_sliding_window=self.sliding_window,
            prefix=f"{prefix}.attn",
            attn_type=AttentionType.DECODER,
            sinks=self.sinks,
        )

    def _apply_qk_norm(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        query = _full_projection_norm(
            query,
            self.q_norm,
            total_heads=self.total_num_heads,
            local_heads=self.num_heads,
            head_dim=self.head_dim,
            tp_size=self.tp_size,
            tp_rank=self.tp_rank,
        )
        key = _full_projection_norm(
            key,
            self.k_norm,
            total_heads=self.total_num_kv_heads,
            local_heads=self.num_kv_heads,
            head_dim=self.head_dim,
            tp_size=self.tp_size,
            tp_rank=self.tp_rank,
        )
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


class Olmo3SinkDFlashMLP(nn.Module):
    def __init__(
        self,
        *,
        config,
        quant_config: QuantizationConfig | None,
        prefix: str,
    ) -> None:
        super().__init__()
        self.gate_up_proj = MergedColumnParallelLinear(
            int(config.hidden_size),
            [int(config.intermediate_size)] * 2,
            bias=False,
            quant_config=quant_config,
            prefix=f"{prefix}.gate_up_proj",
        )
        self.down_proj = RowParallelLinear(
            int(config.intermediate_size),
            int(config.hidden_size),
            bias=False,
            quant_config=quant_config,
            prefix=f"{prefix}.down_proj",
        )
        self.act_fn = SiluAndMul()

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        hidden_states, _ = self.gate_up_proj(hidden_states)
        hidden_states = self.act_fn(hidden_states)
        hidden_states, _ = self.down_proj(hidden_states)
        return hidden_states


class Olmo3SinkDFlashDecoderLayer(nn.Module):
    """One trained OLMo3 post-norm DFlash layer."""

    def __init__(
        self,
        *,
        config,
        cache_config: CacheConfig | None,
        quant_config: QuantizationConfig | None,
        prefix: str,
    ) -> None:
        super().__init__()
        self.self_attn = Olmo3SinkDFlashAttention(
            config=config,
            cache_config=cache_config,
            quant_config=quant_config,
            prefix=f"{prefix}.self_attn",
        )
        self.mlp = Olmo3SinkDFlashMLP(
            config=config,
            quant_config=quant_config,
            prefix=f"{prefix}.mlp",
        )
        self.post_attention_layernorm = RMSNorm(
            int(config.hidden_size),
            eps=float(config.rms_norm_eps),
        )
        self.post_feedforward_layernorm = RMSNorm(
            int(config.hidden_size),
            eps=float(config.rms_norm_eps),
        )

    def forward(
        self,
        positions: torch.Tensor,
        hidden_states: torch.Tensor,
    ) -> torch.Tensor:
        residual = hidden_states
        hidden_states = self.self_attn(positions, hidden_states)
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = residual + hidden_states

        residual = hidden_states
        hidden_states = self.mlp(hidden_states)
        hidden_states = self.post_feedforward_layernorm(hidden_states)
        return residual + hidden_states


@support_torch_compile(
    dynamic_arg_dims={
        "input_ids": 0,
        "positions": 0,
        "input_embeds": 0,
    }
)
class Olmo3SinkDFlashModel(DFlashQwen3Model):
    def __init__(
        self,
        *,
        vllm_config: VllmConfig,
        start_layer_id: int,
        prefix: str,
    ) -> None:
        nn.Module.__init__(self)
        self.config = _draft_config(vllm_config)
        self.vocab_size = int(self.config.vocab_size)
        self.quant_config = get_draft_quant_config(vllm_config)
        options = _draft_options(self.config)
        target_layer_ids = options.get("target_layer_ids") or []
        if not target_layer_ids:
            raise ValueError(
                "OLMo3Sink DFlash requires dflash_config.target_layer_ids"
            )
        self.use_aux_hidden_state = True

        current_config = get_current_vllm_config()
        self.embed_tokens = VocabParallelEmbedding(
            self.vocab_size,
            int(self.config.hidden_size),
            prefix=maybe_prefix(prefix, "embed_tokens"),
        )
        self.mask_token_id = options.get("mask_token_id")
        if self.mask_token_id is None:
            raise ValueError("OLMo3Sink DFlash requires dflash_config.mask_token_id")
        self.mask_embed = nn.Parameter(
            torch.zeros(
                int(self.config.hidden_size),
                dtype=vllm_config.model_config.dtype,
            ),
            requires_grad=False,
        )

        self.layers = nn.ModuleList(
            [
                Olmo3SinkDFlashDecoderLayer(
                    config=self.config,
                    cache_config=current_config.cache_config,
                    quant_config=self.quant_config,
                    prefix=maybe_prefix(
                        prefix,
                        f"layers.{layer_idx + start_layer_id}",
                    ),
                )
                for layer_idx in range(int(self.config.num_hidden_layers))
            ]
        )
        target_hidden_size = int(
            getattr(
                self.config,
                "target_hidden_size",
                vllm_config.model_config.get_hidden_size(),
            )
        )
        self.fc = ReplicatedLinear(
            input_size=target_hidden_size * len(target_layer_ids),
            output_size=int(self.config.hidden_size),
            bias=False,
            params_dtype=vllm_config.model_config.dtype,
            quant_config=self.quant_config,
            prefix=maybe_prefix(prefix, "fc"),
            return_bias=False,
        )
        self.hidden_norm = RMSNorm(
            int(self.config.hidden_size),
            eps=float(self.config.rms_norm_eps),
        )
        self.norm = RMSNorm(
            int(self.config.hidden_size),
            eps=float(self.config.rms_norm_eps),
        )

    def embed_input_ids(self, input_ids: torch.Tensor) -> torch.Tensor:
        embeddings = self.embed_tokens(input_ids)
        mask = (input_ids == int(self.mask_token_id)).unsqueeze(-1)
        return torch.where(mask, self.mask_embed.to(embeddings.dtype), embeddings)

    def _build_context_kv_buffers(
        self,
        layers_attn: list[nn.Module],
        has_bias: bool,
    ) -> None:
        self._hidden_norm_weight = self.hidden_norm.weight.data
        self._fused_kv_weight = torch.cat(
            [attention.qkv_proj.weight[attention.q_size :] for attention in layers_attn],
            dim=0,
        )
        if has_bias:
            self._fused_kv_bias: torch.Tensor | None = torch.cat(
                [
                    attention.qkv_proj.bias[attention.q_size :]
                    for attention in layers_attn
                ],
                dim=0,
            )
        else:
            self._fused_kv_bias = None

    def _normalize_context_k(self, all_k: torch.Tensor) -> torch.Tensor:
        local_shape = all_k.shape
        local_flat = all_k.flatten(-2)
        if get_tensor_model_parallel_world_size() > 1:
            gathered = tensor_model_parallel_all_gather(local_flat.contiguous())
        else:
            gathered = local_flat

        tp_size = get_tensor_model_parallel_world_size()
        tp_rank = get_tensor_model_parallel_rank()
        total_heads = int(self.config.num_key_value_heads)
        local_heads = self.layers[0].self_attn.num_kv_heads
        head_dim = self.layers[0].self_attn.head_dim
        normalized_layers: list[torch.Tensor] = []
        for layer_idx, layer in enumerate(self.layers):
            layer_k = gathered[layer_idx]
            if tp_size <= total_heads:
                normalized = layer.self_attn.k_norm(layer_k)
                if tp_size > 1:
                    normalized = split_tensor_along_last_dim(
                        normalized,
                        tp_size,
                    )[tp_rank]
            else:
                replicas = tp_size // total_heads
                if total_heads * replicas != tp_size or local_heads != 1:
                    raise ValueError(
                        "Unsupported OLMo3Sink DFlash KV-head replication "
                        f"for TP={tp_size}"
                    )
                shape = layer_k.shape[:-1]
                unique = layer_k.view(*shape, tp_size, head_dim)[..., ::replicas, :]
                normalized = layer.self_attn.k_norm(
                    unique.reshape(*shape, total_heads * head_dim)
                )
                head_idx = tp_rank // replicas
                normalized = normalized.view(
                    *shape,
                    total_heads,
                    head_dim,
                )[..., head_idx, :]
            normalized_layers.append(
                normalized.view(local_shape[1], local_heads, head_dim)
            )
        return torch.stack(normalized_layers, dim=0)

    def forward(
        self,
        input_ids: torch.Tensor,
        positions: torch.Tensor,
        input_embeds: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if input_embeds is None:
            input_embeds = self.embed_input_ids(input_ids)
        else:
            mask = (input_ids == int(self.mask_token_id)).unsqueeze(-1)
            input_embeds = torch.where(
                mask,
                self.mask_embed.to(input_embeds.dtype),
                input_embeds,
            )

        hidden_states = input_embeds
        for layer in self.layers:
            hidden_states = layer(positions, hidden_states)
        return self.norm(hidden_states)

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
        expected = {name for name in params if name != "embed_tokens.weight"}
        loaded: set[str] = set()
        tp_rank = get_tensor_model_parallel_rank()
        local_heads = self.layers[0].self_attn.num_heads

        for original_name, loaded_weight in weights:
            name = original_name.removeprefix("model.")
            if "rotary_emb.inv_freq" in name or name == "embed_tokens.weight":
                continue
            if name.endswith(".self_attn.sinks"):
                param = params.get(name)
                if param is None:
                    raise ValueError(f"Unexpected OLMo3Sink DFlash weight {name!r}")
                sink_shard = _select_sink_shard(
                    loaded_weight,
                    total_heads=int(self.config.num_attention_heads),
                    local_heads=local_heads,
                    tp_rank=tp_rank,
                ).to(device=param.device, dtype=param.dtype)
                default_weight_loader(param, sink_shard)
                loaded.add(name)
                continue

            for param_name, weight_name, shard_id in stacked_params_mapping:
                marker = f".{weight_name}."
                if marker not in name:
                    continue
                mapped_name = name.replace(marker, f".{param_name}.")
                param = params.get(mapped_name)
                if param is None:
                    raise ValueError(
                        f"Unexpected OLMo3Sink DFlash weight {original_name!r}"
                    )
                param.weight_loader(param, loaded_weight, shard_id)
                loaded.add(mapped_name)
                break
            else:
                param = params.get(name)
                if param is None:
                    raise ValueError(
                        f"Unexpected OLMo3Sink DFlash weight {original_name!r}"
                    )
                weight_loader = getattr(param, "weight_loader", default_weight_loader)
                weight_loader(param, loaded_weight)
                loaded.add(name)

        missing = expected - loaded
        if missing:
            preview = ", ".join(sorted(missing)[:8])
            raise ValueError(
                "OLMo3Sink DFlash checkpoint is incomplete; missing "
                f"{len(missing)} tensor(s): {preview}"
            )
        logger.info(
            "Loaded %d OLMo3Sink DFlash tensors (%d attention sinks)",
            len(loaded),
            sum(name.endswith(".self_attn.sinks") for name in loaded),
        )
        return loaded


class Olmo3SinkDFlashForCausalLM(DFlashQwen3ForCausalLM):
    """Native-vLLM DFlash shell with an OLMo3Sink draft backbone."""

    has_own_embed_tokens = False
    has_own_lm_head = False

    def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):
        nn.Module.__init__(self)
        speculative_config = vllm_config.speculative_config
        if speculative_config is None or speculative_config.draft_model_config is None:
            raise ValueError("OLMo3Sink DFlash requires a draft model")
        self.draft_model_config = speculative_config.draft_model_config
        self.config = self.draft_model_config.hf_config
        if getattr(self.config, "draft_vocab_size", None) is None:
            self.config.draft_vocab_size = int(self.config.vocab_size)
        target_vocab_size = int(vllm_config.model_config.get_vocab_size())
        if int(self.config.draft_vocab_size) != target_vocab_size:
            raise ValueError(
                "OLMo3Sink DFlash shares the target LM head and requires equal "
                f"vocabularies ({self.config.draft_vocab_size} != {target_vocab_size})"
            )

        target_layer_count = vllm_config.model_config.get_num_layers(
            vllm_config.parallel_config
        )
        self.model = Olmo3SinkDFlashModel(
            vllm_config=vllm_config,
            start_layer_id=target_layer_count,
            prefix=maybe_prefix(prefix, "model"),
        )
        self.lm_head = ParallelLMHead(
            int(self.config.draft_vocab_size),
            int(self.config.hidden_size),
            prefix=maybe_prefix(prefix, "lm_head"),
        )
        self.logits_processor = LogitsProcessor(int(self.config.draft_vocab_size))
        self.draft_id_to_target_id = None

    def embed_input_ids(
        self,
        input_ids: torch.Tensor,
        multimodal_embeddings: NestedTensors | None = None,
        is_multimodal: torch.Tensor | None = None,
    ) -> torch.Tensor:
        return self.model.embed_input_ids(input_ids)

    def load_weights(
        self,
        weights: Iterable[tuple[str, torch.Tensor]],
    ) -> set[str]:
        loaded = self.model.load_weights(weights)
        self.model._build_fused_kv_buffers()
        return {f"model.{name}" for name in loaded}


__all__ = ["Olmo3SinkDFlashForCausalLM"]
