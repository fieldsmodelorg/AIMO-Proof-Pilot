#!/usr/bin/env python3
"""Make DFlash sampling semantics explicit and fail closed.

The deployed DFlash verifier is distribution preserving for temperature plus
either top-p or top-k sampling with acceptance thresholds fixed at one.  Some
other SamplingParams are accepted by stock SGLang but are not implemented by
this linear DFlash path.  Reject those requests instead of silently generating
from a different distribution.  Deterministic inference additionally derives
all verifier coins from the request seed and absolute target positions, so
batch order and unrelated requests cannot perturb a request's output.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


VALIDATION_MARKER = "# DFLASH_SAMPLING_GUARD: reject transforms this verifier cannot preserve."
UNIFORM_MARKER = "# DFLASH_SAMPLING_OPEN_INTERVAL: zero mass must never be accepted."
SEED_MARKER = "# DFLASH_STATELESS_SEED: key verifier coins by request seed and position."
WORKER_SEED_MARKER = "# DFLASH_STATELESS_SEED_CALL: pass absolute verify positions."

VALIDATION_INSERTION = '''    return None
'''

VALIDATION_GUARDS = '''    # DFLASH_SAMPLING_GUARD: reject transforms this verifier cannot preserve.
    params = req.sampling_params
    if float(getattr(params, "min_p", 0.0)) != 0.0:
        return "DFLASH speculative decoding does not support min_p sampling yet."

    if int(getattr(params, "min_new_tokens", 0)) != 0:
        return (
            "DFLASH speculative decoding does not support min_new_tokens yet "
            "because the constraint can change inside a verify block."
        )

    if (
        float(getattr(params, "frequency_penalty", 0.0)) != 0.0
        or float(getattr(params, "presence_penalty", 0.0)) != 0.0
        or float(getattr(params, "repetition_penalty", 1.0)) != 1.0
    ):
        return (
            "DFLASH speculative decoding does not support frequency, presence, "
            "or repetition penalties yet because penalty state changes inside "
            "a verify block."
        )

    top_k = int(getattr(params, "top_k", 1 << 30))
    top_p = float(getattr(params, "top_p", 1.0))
    if 1 < top_k < (1 << 30) and top_p < 1.0:
        return (
            "DFLASH speculative decoding does not support combined top_k and "
            "top_p yet because its filtering order differs from the target sampler."
        )

    if getattr(req, "custom_logit_processor", None) is not None:
        return "DFLASH speculative decoding does not support custom logit processors yet."

    return None
'''

UNIFORM_INSERTION = '''    need_top_k = bool(getattr(sampling_info, "need_top_k_sampling", True))
'''

OPEN_INTERVAL_GUARD = '''    # DFLASH_SAMPLING_OPEN_INTERVAL: zero mass must never be accepted.
    # torch.rand is uniform on [0, 1). Move only its zero endpoint to one,
    # producing the same discrete uniform grid on (0, 1] without perturbing
    # any valid positive coin or biasing tiny nonzero target probabilities.
    uniform_samples.masked_fill_(uniform_samples == 0, 1.0)
    uniform_samples_for_final_sampling.masked_fill_(
        uniform_samples_for_final_sampling == 0, 1.0
    )
'''
UNIFORM_GUARD = OPEN_INTERVAL_GUARD + "\n" + UNIFORM_INSERTION

LEGACY_SUBNORMAL_GUARD = '''    # DFLASH_SAMPLING_OPEN_INTERVAL: zero mass must never be accepted.
    # The CUDA verifier uses <= at its CDF boundary.  torch.rand can return
    # exactly zero, so move both injected and generated coins into (0, 1].
    smallest_positive = torch.nextafter(
        torch.zeros((), dtype=torch.float32, device=device),
        torch.ones((), dtype=torch.float32, device=device),
    )
    uniform_samples.clamp_min_(smallest_positive)
    uniform_samples_for_final_sampling.clamp_min_(smallest_positive)
'''
LEGACY_EPSILON_GUARD = '''    # DFLASH_SAMPLING_OPEN_INTERVAL: zero mass must never be accepted.
    # The CUDA verifier uses <= at its CDF boundary.  torch.rand can return
    # exactly zero, so move both injected and generated coins into (0, 1].
    # Use epsilon rather than the smallest subnormal: GPU kernels may flush
    # subnormals to zero, recreating the zero-probability acceptance bug.
    smallest_positive = torch.finfo(torch.float32).eps
    uniform_samples.clamp_min_(smallest_positive)
    uniform_samples_for_final_sampling.clamp_min_(smallest_positive)
'''

HASH_IMPORT_OLD = '''from sglang.srt.layers.sampler import apply_custom_logit_processor
'''
HASH_IMPORT_NEW = '''from sglang.srt.layers.sampler import apply_custom_logit_processor
from sglang.srt.layers.utils.hash import murmur_hash32
'''

SIGNATURE_OLD = '''    sampling_info: Any,
    max_top_k: Optional[int] = None,
'''
SIGNATURE_NEW = '''    sampling_info: Any,
    verify_positions: Optional[torch.Tensor] = None,
    max_top_k: Optional[int] = None,
'''

ACCEPT_UNIFORMS_OLD = '''    device = next_token_logits.device

    if uniform_samples is None:
        uniform_samples = torch.rand(
            (bs, draft_token_num), dtype=torch.float32, device=device
        )
    else:
'''
ACCEPT_UNIFORMS_NEW = '''    device = next_token_logits.device

    # DFLASH_STATELESS_SEED: key verifier coins by request seed and position.
    sampling_seed = getattr(sampling_info, "sampling_seed", None)
    seeded_positions = None
    needs_seeded_uniforms = sampling_seed is not None and (
        uniform_samples is None
        or uniform_samples_for_final_sampling is None
    )
    if needs_seeded_uniforms:
        if sampling_seed.ndim != 1 or sampling_seed.shape[0] != bs:
            raise ValueError(
                "sampling_seed shape mismatch. "
                f"Expected {(bs,)}, got {tuple(sampling_seed.shape)}."
            )
        if verify_positions is None:
            raise ValueError(
                "DFLASH deterministic sampling requires absolute verify_positions."
            )
        if verify_positions.shape != (bs, draft_token_num):
            raise ValueError(
                "verify_positions shape mismatch. "
                f"Expected {(bs, draft_token_num)}, "
                f"got {tuple(verify_positions.shape)}."
            )
        sampling_seed = sampling_seed.to(device=device, dtype=torch.int64)
        seeded_positions = verify_positions.to(device=device, dtype=torch.int64)

    def make_seeded_uniforms(
        seeds: torch.Tensor,
        positions: torch.Tensor,
        *,
        stream: int,
        output_shape: tuple[int, ...],
    ) -> torch.Tensor:
        stream_ids = torch.tensor(
            [stream], dtype=torch.int64, device=device
        )
        hashed = murmur_hash32(seeds, positions, stream_ids)
        # Map every uint32 hash bijectively onto {1/2^32, ..., 1}.  Float64
        # preserves the +1 before the verifier's required float32 conversion.
        return (
            (hashed.to(torch.float64) + 1.0)
            .mul_(1.0 / 4294967296.0)
            .to(torch.float32)
            .reshape(output_shape)
        )

    if uniform_samples is None:
        if sampling_seed is None:
            uniform_samples = torch.rand(
                (bs, draft_token_num), dtype=torch.float32, device=device
            )
        else:
            assert seeded_positions is not None
            uniform_samples = make_seeded_uniforms(
                sampling_seed[:, None]
                .expand(-1, draft_token_num)
                .reshape(-1),
                seeded_positions.reshape(-1),
                stream=0,
                output_shape=(bs, draft_token_num),
            )
    else:
'''

FINAL_UNIFORMS_OLD = '''    if uniform_samples_for_final_sampling is None:
        uniform_samples_for_final_sampling = torch.rand(
            (bs,), dtype=torch.float32, device=device
        )
    else:
'''
FINAL_UNIFORMS_NEW = '''    if uniform_samples_for_final_sampling is None:
        if sampling_seed is None:
            uniform_samples_for_final_sampling = torch.rand(
                (bs,), dtype=torch.float32, device=device
            )
        else:
            assert seeded_positions is not None
            uniform_samples_for_final_sampling = make_seeded_uniforms(
                sampling_seed,
                seeded_positions[:, 0].contiguous(),
                stream=1,
                output_shape=(bs,),
            )
    else:
'''

LEGACY_SEED_GATE = '''    sampling_seed = getattr(sampling_info, "sampling_seed", None)
    seeded_positions = None
    if sampling_seed is not None:
'''
CURRENT_SEED_GATE = '''    sampling_seed = getattr(sampling_info, "sampling_seed", None)
    seeded_positions = None
    needs_seeded_uniforms = sampling_seed is not None and (
        uniform_samples is None
        or uniform_samples_for_final_sampling is None
    )
    if needs_seeded_uniforms:
'''

WORKER_CALL_OLD = '''                sampling_info=sampling_info,
                max_top_k=draft_input.max_top_k,
'''
WORKER_CALL_NEW = '''                sampling_info=sampling_info,
                # DFLASH_STATELESS_SEED_CALL: pass absolute verify positions.
                verify_positions=positions_2d,
                max_top_k=draft_input.max_top_k,
'''


def patch_dflash_utils_text(text: str) -> str:
    patched = text.replace(LEGACY_SUBNORMAL_GUARD, OPEN_INTERVAL_GUARD, 1)
    patched = patched.replace(LEGACY_EPSILON_GUARD, OPEN_INTERVAL_GUARD, 1)
    if VALIDATION_MARKER not in patched:
        function_start = patched.find("def validate_dflash_request(")
        if function_start < 0:
            raise RuntimeError("Could not locate validate_dflash_request.")
        return_pos = patched.find(VALIDATION_INSERTION, function_start)
        if return_pos < 0:
            raise RuntimeError("Could not locate validate_dflash_request return.")
        patched = (
            patched[:return_pos]
            + VALIDATION_GUARDS
            + patched[return_pos + len(VALIDATION_INSERTION) :]
        )

    if UNIFORM_MARKER not in patched:
        function_start = patched.find(
            "def compute_dflash_sampling_correct_drafts_and_bonus("
        )
        if function_start < 0:
            raise RuntimeError("Could not locate DFlash sampling verifier.")
        insertion_pos = patched.find(UNIFORM_INSERTION, function_start)
        if insertion_pos < 0:
            raise RuntimeError("Could not locate DFlash sampling uniforms.")
        patched = (
            patched[:insertion_pos]
            + UNIFORM_GUARD
            + patched[insertion_pos + len(UNIFORM_INSERTION) :]
        )
    return patched


def patch_dflash_seeded_sampling_text(text: str) -> str:
    """Patch the real DFlash verifier with stateless seeded-uniform support."""

    patched = text.replace(LEGACY_SEED_GATE, CURRENT_SEED_GATE, 1)
    if SEED_MARKER in patched:
        required = (
            "verify_positions",
            "murmur_hash32",
            "make_seeded_uniforms",
            "needs_seeded_uniforms",
        )
        missing = [needle for needle in required if needle not in patched]
        if missing:
            raise RuntimeError(
                "DFLASH seeded-sampling marker is present but code is incomplete: "
                f"{missing}."
            )
        return patched

    replacements = (
        (HASH_IMPORT_OLD, HASH_IMPORT_NEW, "DFlash hash import"),
        (SIGNATURE_OLD, SIGNATURE_NEW, "DFlash sampling signature"),
        (ACCEPT_UNIFORMS_OLD, ACCEPT_UNIFORMS_NEW, "DFlash acceptance uniforms"),
        (FINAL_UNIFORMS_OLD, FINAL_UNIFORMS_NEW, "DFlash final uniform"),
    )
    for old, new, description in replacements:
        count = patched.count(old)
        if count != 1:
            raise RuntimeError(
                f"Could not locate exactly one {description}; found {count}. "
                "The SGLang source layout changed."
            )
        patched = patched.replace(old, new, 1)
    return patched


def patch_dflash_worker_text(text: str) -> str:
    """Pass the worker's absolute block positions into seeded verification."""

    if WORKER_SEED_MARKER in text:
        if "verify_positions=positions_2d" not in text:
            raise RuntimeError(
                "DFLASH worker seed marker is present without verify_positions."
            )
        return text
    count = text.count(WORKER_CALL_OLD)
    if count != 1:
        raise RuntimeError(
            "Could not locate exactly one DFlash sampling verifier call; "
            f"found {count}. The SGLang source layout changed."
        )
    return text.replace(WORKER_CALL_OLD, WORKER_CALL_NEW, 1)


def _patch_file(path: Path, transform, backup_suffix: str) -> None:
    original = path.read_text()
    patched = transform(original)
    if patched != original:
        backup = path.with_suffix(path.suffix + backup_suffix)
        if not backup.exists():
            shutil.copy2(path, backup)
        path.write_text(patched)
        print(f"  patched: {path.relative_to(path.parents[2])}")
    else:
        print(f"  verified: {path.relative_to(path.parents[2])}")


def patch_venv(venv: Path) -> None:
    roots = list(venv.glob("lib/python*/site-packages/sglang/srt"))
    if len(roots) != 1:
        raise RuntimeError(f"Expected one sglang/srt under {venv}, found {roots}")
    utils_path = roots[0] / "speculative/dflash_utils.py"
    _patch_file(
        utils_path,
        lambda text: patch_dflash_seeded_sampling_text(
            patch_dflash_utils_text(text)
        ),
        ".pre_sampling_guard",
    )
    _patch_file(
        roots[0] / "speculative/dflash_worker_v2.py",
        patch_dflash_worker_text,
        ".pre_seeded_sampling",
    )
    for pyc in (roots[0] / "speculative").rglob("*.pyc"):
        pyc.unlink()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <venv_path>")
    patch_venv(Path(sys.argv[1]).resolve())
    print("[patch] DFlash sampling guards verified")


if __name__ == "__main__":
    main()
