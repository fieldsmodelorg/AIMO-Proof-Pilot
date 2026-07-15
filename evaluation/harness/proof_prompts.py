"""Verbatim ycchen Math-3R prompts, renderers, bundles, and XML parsers.

The templates are copied byte-for-byte from ycchen-tw/proof-pilot-codes commit
bc03a2c71a076990deaad3d712c6889682e12c69.  The same files occur in both
``distill_gen/math_3r/prompts`` and ``kaggle/proof_agent/prompts`` there.
"""

from __future__ import annotations

import hashlib
import re
from functools import lru_cache
from pathlib import Path

PROMPT_ROOT = Path(__file__).resolve().parent.parent / "prompts" / "ycchen_math_3r"
PROMPT_SOURCE_COMMIT = "bc03a2c71a076990deaad3d712c6889682e12c69"
SYSTEM_DELIMITER = "===SYSTEM==="
USER_DELIMITER = "===USER==="

_GENERATION = re.compile(
    r"\s*<solution>(.*?)</solution>\s*"
    r"<self_evaluation>(.*?)</self_evaluation>\s*"
    r"<score>\s*(0(?:\.5)?|1)\s*</score>\s*",
    re.DOTALL,
)
_VERIFICATION = re.compile(
    r"\s*<evaluation>(.*?)</evaluation>\s*"
    r"<suggestions>(.*?)</suggestions>\s*"
    r"<score>\s*(0(?:\.5)?|1)\s*</score>\s*",
    re.DOTALL,
)


@lru_cache(maxsize=None)
def template(name: str) -> str:
    return (PROMPT_ROOT / name).read_text()


def prompt_hashes() -> dict[str, str]:
    return {
        name: hashlib.sha256((PROMPT_ROOT / name).read_bytes()).hexdigest()
        for name in ("prover.txt", "verifier.txt", "refiner.txt")
    }


def _messages(rendered: str) -> list[dict[str, str]]:
    system, user = rendered.split(USER_DELIMITER, 1)
    if not system.startswith(SYSTEM_DELIMITER):
        raise ValueError("ycchen prompt lacks the system delimiter")
    return [
        {"role": "system", "content": system.removeprefix(SYSTEM_DELIMITER).strip()},
        {"role": "user", "content": user.strip()},
    ]


def generation_messages(problem: str) -> list[dict[str, str]]:
    return _messages(template("prover.txt").replace("{problem}", problem))


def verification_messages(
    problem: str,
    proof: str,
    self_evaluation: str,
) -> list[dict[str, str]]:
    rendered = (
        template("verifier.txt")
        .replace("{problem}", problem)
        .replace("{candidate_solution}", proof)
        .replace("{candidate_self_eval}", self_evaluation)
    )
    return _messages(rendered)


def refinement_messages(
    problem: str,
    candidate_id: str,
    proof: str,
    self_evaluation: str,
    review_score: float,
    review: str,
) -> list[dict[str, str]]:
    parts = [
        f'<candidate id="{candidate_id}">',
        "<proof>",
        proof,
        "</proof>",
        f'<verifier_review score="{review_score:g}">',
        review,
        "</verifier_review>",
        "<self_evaluation>",
        self_evaluation,
        "</self_evaluation>",
        "</candidate>",
    ]
    rendered = (
        template("refiner.txt")
        .replace("{problem}", problem)
        .replace("{candidate_bundle}", "\n".join(parts))
    )
    return _messages(rendered)


def parse_generation(text: str) -> tuple[str, str, float]:
    match = _GENERATION.fullmatch(text)
    if match is None:
        raise ValueError("generation does not match ycchen's XML contract")
    proof, self_evaluation, score = match.groups()
    proof = proof.strip()
    self_evaluation = self_evaluation.strip()
    if not proof or not self_evaluation:
        raise ValueError("generation contains an empty required XML element")
    return proof, self_evaluation, float(score)


def parse_verification(text: str) -> tuple[str, float]:
    match = _VERIFICATION.fullmatch(text)
    if match is None:
        raise ValueError("verification does not match ycchen's XML contract")
    evaluation, suggestions, score = match.groups()
    if not evaluation.strip() or not suggestions.strip():
        raise ValueError("verification contains an empty required XML element")
    return text.strip(), float(score)
