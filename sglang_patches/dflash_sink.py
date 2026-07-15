# Adapted from sglang srt/models/dflash.py (DFlashDraftModel) + the proof-pilot
# olmo2_sink.py target patch. This is the DFlash DRAFT model rewritten to the
# OLMo3 + attention-sink architecture so the trained NoDupFA3Draft weights load
# and run faithfully under sglang's native DFlash worker.
#
# Deltas vs stock srt/models/dflash.py (which is Qwen3-flavored):
#   - attention sink (per-Q-head s_aux), passed into RadixAttention (the "特規")
#   - OLMo3 post-norm decoder layer (post_attention + post_feedforward LN, no
#     input_layernorm) instead of Qwen3 pre-norm
#   - full-projection QK-norm (RMSNorm over heads*head_dim) instead of per-head
#   - all-SWA: sliding_window on every draft layer (trained no-dup layout)
#   - learnable mask_embed substituted at mask positions (vs target-embedded
#     mask token) -- done inside forward(), no worker patch needed
#
# Preserves the worker-called interface verbatim: DFlashAttention.{forward,
# kv_proj_only, apply_k_norm, apply_k_rope}; DFlashDraftModel.{project_target_hidden,
# forward(...,input_embeds), load_weights, block_size}; EntryClass.
#
# Supports tensor parallelism using the same head sharding and full-projection
# QK-normalization collectives as the OLMo3 target implementation.

from __future__ import annotations

import logging
from functools import partial
from typing import Iterable, Optional, Tuple

import torch
import torch.nn.functional as F
from torch import nn

from sglang.srt.distributed import (
    get_tensor_model_parallel_rank,
    get_tensor_model_parallel_world_size,
    split_tensor_along_last_dim,
    tensor_model_parallel_all_gather,
)
from sglang.srt.layers.activation import SiluAndMul
from sglang.srt.layers.layernorm import RMSNorm
from sglang.srt.layers.linear import (
    MergedColumnParallelLinear,
    QKVParallelLinear,
    RowParallelLinear,
)
from sglang.srt.layers.logits_processor import LogitsProcessorOutput
from sglang.srt.layers.radix_attention import AttentionType, RadixAttention
from sglang.srt.layers.rotary_embedding import get_rope
from sglang.srt.model_executor.forward_batch_info import ForwardBatch
from sglang.srt.model_loader.weight_utils import default_weight_loader
from sglang.srt.server_args import get_global_server_args
from sglang.srt.speculative.dflash_utils import (
    can_dflash_slice_qkv_weight,
    parse_dflash_draft_config,
)

logger = logging.getLogger(__name__)


def _rope_theta(config) -> float:
    rp = getattr(config, "rope_parameters", None)
    if isinstance(rp, dict) and "rope_theta" in rp:
        return float(rp["rope_theta"])
    return float(getattr(config, "rope_theta", 500000))


class DFlashAttention(nn.Module):
    """OLMo3 + sink attention for the DFlash draft block.

    Block queries attend over [context K/V already in the draft KV cache | the
    block's own K/V]; the per-head sink adds an extra softmax logit column.
    """

    def __init__(self, config, layer_id: int) -> None:
        super().__init__()
        hidden_size = int(config.hidden_size)
        self.tp_size = int(get_tensor_model_parallel_world_size())
        self.tp_rank = int(get_tensor_model_parallel_rank())
        self.config = config
        self.total_num_heads = int(config.num_attention_heads)
        self.total_num_kv_heads = int(getattr(config, "num_key_value_heads", self.total_num_heads))
        assert self.total_num_heads % self.tp_size == 0
        self.num_heads = self.total_num_heads // self.tp_size
        if self.total_num_kv_heads >= self.tp_size:
            assert self.total_num_kv_heads % self.tp_size == 0
        else:
            assert self.tp_size % self.total_num_kv_heads == 0
        self.num_kv_heads = max(1, self.total_num_kv_heads // self.tp_size)
        self.head_dim = int(getattr(config, "head_dim", hidden_size // self.total_num_heads))
        self.q_size = self.num_heads * self.head_dim
        self.kv_size = self.num_kv_heads * self.head_dim
        rms_norm_eps = float(getattr(config, "rms_norm_eps", 1e-6))
        attention_bias = bool(getattr(config, "attention_bias", False))

        self.qkv_proj = QKVParallelLinear(
            hidden_size, self.head_dim, self.total_num_heads,
            total_num_kv_heads=self.total_num_kv_heads, bias=attention_bias, prefix="qkv_proj",
        )
        self.o_proj = RowParallelLinear(
            self.total_num_heads * self.head_dim, hidden_size, bias=attention_bias, prefix="o_proj",
        )
        # Full-projection QK-norm (OLMo3), not per-head.
        self.q_norm = RMSNorm(self.total_num_heads * self.head_dim, eps=rms_norm_eps)
        self.k_norm = RMSNorm(self.total_num_kv_heads * self.head_dim, eps=rms_norm_eps)

        # All-SWA: default (unscaled) RoPE on every layer (trained no-dup layout).
        self.rotary_emb = get_rope(
            self.head_dim, rotary_dim=self.head_dim,
            max_position=int(getattr(config, "max_position_embeddings", 65536)),
            base=_rope_theta(config), rope_scaling={"rope_type": "default"},
        )

        # Attention sink: per-Q-head scalar (gpt-oss style).
        attn_backend = get_global_server_args().attention_backend
        sinks_dtype = torch.float32 if attn_backend == "trtllm_mha" else torch.bfloat16
        self.sinks = nn.Parameter(torch.empty(self.num_heads, dtype=sinks_dtype), requires_grad=False)

        self.scaling = self.head_dim**-0.5
        # All-SWA window. Read robustly: some config classes (e.g. Qwen3Config used
        # only for parsing) null a top-level `sliding_window`, so fall back to the
        # preserved dflash_config dict.
        sw = getattr(config, "sliding_window", None)
        if sw is None:
            dcfg = getattr(config, "dflash_config", {}) or {}
            sw = dcfg.get("sliding_window", 128)
        sliding_window = int(sw) - 1  # sglang exclusive
        self.attn = RadixAttention(
            num_heads=self.num_heads, head_dim=self.head_dim, scaling=self.scaling,
            num_kv_heads=self.num_kv_heads, layer_id=layer_id,
            sliding_window_size=sliding_window, attn_type=AttentionType.ENCODER_ONLY,
        )

    def _apply_qk_norm(
        self, q: torch.Tensor, k: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.tp_size > 1:
            q = tensor_model_parallel_all_gather(q.contiguous())
            k = tensor_model_parallel_all_gather(k.contiguous())
        q = self.q_norm.forward_native(q)
        k = self.k_norm.forward_native(k)
        if self.tp_size > 1:
            splitter = partial(split_tensor_along_last_dim, num_partitions=self.tp_size)
            q = splitter(q)[self.tp_rank]
            k = splitter(k)[self.tp_rank]
        return q, k

    def forward(self, positions, hidden_states, forward_batch: ForwardBatch) -> torch.Tensor:
        qkv, _ = self.qkv_proj(hidden_states)
        q, k, v = qkv.split([self.q_size, self.kv_size, self.kv_size], dim=-1)
        q, k = self._apply_qk_norm(q, k)
        q, k = self.rotary_emb(positions, q, k)
        attn_output = self.attn(q, k, v, forward_batch, sinks=self.sinks)
        output, _ = self.o_proj(attn_output)
        return output

    # ---- worker interface: materialize context (target hidden) into draft KV --
    def kv_proj_only(self, hidden_states: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        can_slice, _ = can_dflash_slice_qkv_weight(self.qkv_proj)
        if can_slice:
            kv_slice = slice(self.q_size, self.q_size + 2 * self.kv_size)
            weight = self.qkv_proj.weight[kv_slice]
            bias = self.qkv_proj.bias[kv_slice] if self.qkv_proj.bias is not None else None
            kv = F.linear(hidden_states, weight, bias)
            k, v = kv.split([self.kv_size, self.kv_size], dim=-1)
            return k, v
        qkv, _ = self.qkv_proj(hidden_states)
        _, k, v = qkv.split([self.q_size, self.kv_size, self.kv_size], dim=-1)
        return k, v

    def apply_k_norm(self, k: torch.Tensor) -> torch.Tensor:
        # Full-projection k_norm (OLMo3), matching forward().
        if self.tp_size > 1:
            k = tensor_model_parallel_all_gather(k.contiguous())
        k = self.k_norm.forward_native(k)
        if self.tp_size > 1:
            k = split_tensor_along_last_dim(k, self.tp_size)[self.tp_rank]
        return k

    def apply_k_rope(self, positions: torch.Tensor, k: torch.Tensor) -> torch.Tensor:
        dummy_q = k.new_empty(k.shape)
        _, k = self.rotary_emb(positions, dummy_q, k)
        return k


class DFlashMLP(nn.Module):
    def __init__(self, config, quant_config=None, prefix: str = "") -> None:
        super().__init__()
        hidden_size = int(config.hidden_size)
        intermediate_size = int(config.intermediate_size)
        self.gate_up_proj = MergedColumnParallelLinear(
            hidden_size, [intermediate_size] * 2, bias=False,
            quant_config=quant_config, prefix=f"{prefix}.gate_up_proj" if prefix else "gate_up_proj",
        )
        self.down_proj = RowParallelLinear(
            intermediate_size, hidden_size, bias=False,
            quant_config=quant_config, prefix=f"{prefix}.down_proj" if prefix else "down_proj",
        )
        # The draft checkpoint is W4A16: its MLP weights are INT4 but its
        # activations remain BF16. The target-only Humming helper uses this
        # explicit role marker to leave both draft projections on W4A16.
        self.gate_up_proj._dflash_draft_mlp = True
        self.down_proj._dflash_draft_mlp = True
        self.act_fn = SiluAndMul()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gate_up, _ = self.gate_up_proj(x)
        x = self.act_fn(gate_up)
        x, _ = self.down_proj(x)
        return x


class DFlashDecoderLayer(nn.Module):
    """OLMo3 post-norm decoder layer (no input_layernorm)."""

    def __init__(self, config, layer_id: int, quant_config=None, prefix: str = "") -> None:
        super().__init__()
        rms_norm_eps = float(getattr(config, "rms_norm_eps", 1e-6))
        self.self_attn = DFlashAttention(config=config, layer_id=layer_id)
        # MLP-only quantization: thread quant_config to the MLP (gate_up/down) so a
        # compressed-tensors (e.g. int4-w4a16) draft checkpoint loads marlin weights.
        # self_attn stays bf16 (the quant config ignores self_attn) -> keeps DFlash
        # fused-KV materialization on (it disables when qkv is quantized).
        self.mlp = DFlashMLP(config=config, quant_config=quant_config,
                             prefix=f"{prefix}.mlp" if prefix else "mlp")
        self.post_attention_layernorm = RMSNorm(config.hidden_size, eps=rms_norm_eps)
        self.post_feedforward_layernorm = RMSNorm(config.hidden_size, eps=rms_norm_eps)

    def forward(self, positions, hidden_states, forward_batch: ForwardBatch) -> torch.Tensor:
        if hidden_states.numel() == 0:
            return hidden_states
        residual = hidden_states
        hidden_states = self.self_attn(positions, hidden_states, forward_batch)
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states = residual + hidden_states
        residual = hidden_states
        hidden_states = self.mlp(hidden_states)
        hidden_states = self.post_feedforward_layernorm(hidden_states)
        hidden_states = residual + hidden_states
        return hidden_states


class DFlashDraftModel(nn.Module):
    """OLMo3 + sink DFlash draft (no embedding / lm_head; uses the target's)."""

    def __init__(self, config, quant_config=None, prefix: str = "") -> None:
        super().__init__()
        self.config = config
        hidden_size = int(config.hidden_size)
        num_layers = int(config.num_hidden_layers)
        rms_norm_eps = float(getattr(config, "rms_norm_eps", 1e-6))

        self.layers = nn.ModuleList(
            [DFlashDecoderLayer(config=config, layer_id=i, quant_config=quant_config,
                                prefix=f"layers.{i}") for i in range(num_layers)]
        )
        self.norm = RMSNorm(hidden_size, eps=rms_norm_eps)

        draft_config = parse_dflash_draft_config(draft_hf_config=config)
        target_num_layers = (
            int(draft_config.num_target_layers)
            if draft_config.num_target_layers is not None else num_layers
        )
        target_layer_ids = draft_config.resolve_target_layer_ids(
            target_num_layers=target_num_layers, draft_num_layers=num_layers
        )
        self.num_context_features = int(len(target_layer_ids))
        self.fc = nn.Linear(self.num_context_features * hidden_size, hidden_size, bias=False)
        self.hidden_norm = RMSNorm(hidden_size, eps=rms_norm_eps)
        self.block_size = draft_config.resolve_block_size(default=16)

        # Learnable mask embedding (trained), substituted at mask positions.
        self.mask_embed = nn.Parameter(torch.zeros(hidden_size))
        self.mask_token_id = draft_config.mask_token_id

    def get_attention_sliding_window_size(self):
        # Draft is all-SWA. Expose the window so the model runner carries the
        # correct sliding-window metadata. If top-level parsing leaves the value
        # unset, read the checkpoint's dflash_config.
        # sglang window is exclusive (HF inclusive), so -1, matching the layers.
        sw = getattr(self.config, "sliding_window", None)
        if sw is None:
            dcfg = getattr(self.config, "dflash_config", {}) or {}
            sw = dcfg.get("sliding_window", 128)
        return int(sw) - 1

    def project_target_hidden(self, target_hidden: torch.Tensor) -> torch.Tensor:
        expected = int(self.fc.in_features)
        if target_hidden.ndim != 2 or int(target_hidden.shape[-1]) != expected:
            raise ValueError(
                f"DFLASH target_hidden dim mismatch: expected [N, {expected}], "
                f"got {tuple(target_hidden.shape)}"
            )
        return self.hidden_norm(self.fc(target_hidden))

    @torch.no_grad()
    def forward(
        self,
        input_ids: torch.Tensor,
        positions: torch.Tensor,
        forward_batch: ForwardBatch,
        input_embeds: Optional[torch.Tensor] = None,
        get_embedding: bool = False,
        pp_proxy_tensors=None,
    ) -> LogitsProcessorOutput:
        if input_embeds is None:
            raise ValueError("DFlashDraftModel requires input_embeds (target embedding).")
        hidden_states = input_embeds
        # Substitute the learnable mask_embed at mask positions (the trained draft
        # queries are all mask_embed; sglang seeds them with target_embed(mask_id)).
        if input_ids is not None and self.mask_token_id is not None and hidden_states.numel():
            # Unconditional torch.where (no .any() host-sync, which is illegal
            # during cuda-graph capture).
            mask = (input_ids == int(self.mask_token_id)).unsqueeze(-1)
            hidden_states = torch.where(
                mask, self.mask_embed.to(hidden_states.dtype), hidden_states
            )

        for layer in self.layers:
            hidden_states = layer(positions, hidden_states, forward_batch)
        if hidden_states.numel() != 0:
            hidden_states = self.norm(hidden_states)
        return LogitsProcessorOutput(next_token_logits=None, hidden_states=hidden_states)

    def load_weights(self, weights: Iterable[Tuple[str, torch.Tensor]]):
        stacked_params_mapping = [
            ("qkv_proj", "q_proj", "q"),
            ("qkv_proj", "k_proj", "k"),
            ("qkv_proj", "v_proj", "v"),
            ("gate_up_proj", "gate_proj", 0),
            ("gate_up_proj", "up_proj", 1),
        ]
        params_dict = dict(self.named_parameters())

        def resolve(name):
            if name in params_dict:
                return name
            if name.startswith("model.") and name[6:] in params_dict:
                return name[6:]
            if f"model.{name}" in params_dict:
                return f"model.{name}"
            return None

        loaded_sinks = 0
        for name, loaded_weight in weights:
            if "rotary_emb.inv_freq" in name:
                continue
            if "self_attn.sinks" in name:
                rname = resolve(name)
                param = params_dict[rname]
                start = get_tensor_model_parallel_rank() * param.numel()
                param.data.copy_(loaded_weight[start : start + param.numel()].to(param.dtype))
                loaded_sinks += 1
                continue
            for param_name, weight_name, shard_id in stacked_params_mapping:
                if f".{weight_name}." not in name:
                    continue
                rname = resolve(name.replace(weight_name, param_name))
                if rname is None:
                    continue
                param = params_dict[rname]
                param.weight_loader(param, loaded_weight, shard_id)
                break
            else:
                rname = resolve(name)
                if rname is None:
                    continue
                param = params_dict[rname]
                if rname.endswith("fc.weight") and tuple(loaded_weight.shape) != tuple(param.shape):
                    raise ValueError(
                        f"DFLASH fc.weight shape mismatch: expected {tuple(param.shape)}, "
                        f"got {tuple(loaded_weight.shape)}"
                    )
                weight_loader = getattr(param, "weight_loader", default_weight_loader)
                weight_loader(param, loaded_weight)
        logger.info(f"dflash_sink: loaded {loaded_sinks} attention-sink tensors")


EntryClass = DFlashDraftModel
