"""YAML-driven generate-verify-refine proof-pool search."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import random
from collections import Counter
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any

from async_client import AsyncChatClient
from loop_detect import is_degenerate
from proof_prompts import (
    generation_messages,
    parse_generation,
    parse_selected_id,
    parse_verification,
    refinement_messages,
    selection_bundle,
    selector_messages,
    verification_messages,
)

# The final LLM selector is a discrete pick-an-id task -> low temperature for format
# stability (ycchen ran select/ at low temp), independent of the search temperature.
SELECTION_TEMPERATURE = 0.3


def stable_seed(base: int, *parts: str) -> int:
    material = "\0".join([str(base), *parts]).encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big") % (2**31 - 1)


def majority_winner(votes: list[str | None], rank_order: list[str]) -> str | None:
    """The most-voted id; ties broken by rank_order (earliest = highest-ranked wins).
    None if there are no non-null votes. Pure helper so it can be unit-tested."""
    valid = [v for v in votes if v is not None]
    if not valid:
        return None
    counts = Counter(valid)
    top = max(counts.values())
    for proof_id in rank_order:
        if counts.get(proof_id, 0) == top:
            return proof_id
    return None


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    os.replace(temporary, path)


@dataclass(frozen=True)
class CallSpec:
    sample_id: str
    stage: str
    messages: list[dict[str, str]]
    seed: int


@dataclass(frozen=True)
class Candidate:
    proof_id: str
    round_index: int
    parent_id: str | None
    generation: CallSpec


@dataclass(frozen=True)
class Verification:
    sample_id: str
    score: float
    analysis: str


@dataclass
class Proof:
    proof_id: str
    round_index: int
    parent_id: str | None
    proof: str
    self_evaluation: str
    self_score: float
    generation_sample_id: str
    verifications: list[Verification] = field(default_factory=list)

    @property
    def mean_score(self) -> float:
        if not self.verifications:
            raise RuntimeError(f"proof {self.proof_id} has no verification scores")
        return mean(item.score for item in self.verifications)

    def to_dict(self) -> dict:
        value = asdict(self)
        value["mean_score"] = self.mean_score if self.verifications else None
        return value

    @classmethod
    def from_dict(cls, value: dict) -> "Proof":
        return cls(
            proof_id=value["proof_id"],
            round_index=value["round_index"],
            parent_id=value["parent_id"],
            proof=value["proof"],
            self_evaluation=value["self_evaluation"],
            self_score=value["self_score"],
            generation_sample_id=value["generation_sample_id"],
            verifications=[Verification(**item) for item in value["verifications"]],
        )


class CallStore:
    def __init__(self, root: Path):
        self.path = root / "calls.jsonl"
        self.prompts = root / "prompts"
        self.prompts.mkdir(parents=True, exist_ok=True)
        self.records: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("error") is not None:
                    # A persisted FAILED call -- typically a transient failure
                    # (e.g. the SGLang server crashed mid-run, leaving every
                    # in-flight call recorded with a RemoteProtocolError). Skip
                    # it so a resume RE-ATTEMPTS the call instead of re-raising
                    # the old error and aborting again. The failed line stays in
                    # calls.jsonl as an audit trail; a later success for the same
                    # sample_id supersedes it (loaded below).
                    continue
                sample_id = record["sample_id"]
                if sample_id in self.records:
                    raise RuntimeError(f"duplicate persisted sample ID: {sample_id}")
                self.records[sample_id] = record
        self._lock = asyncio.Lock()

    def _save_prompt(self, messages: list[dict[str, str]]) -> str:
        encoded = json.dumps(messages, sort_keys=True, ensure_ascii=False).encode()
        digest = hashlib.sha256(encoded).hexdigest()
        path = self.prompts / f"{digest}.json"
        if not path.exists():
            atomic_json(path, messages)
        return digest

    async def _append(self, record: dict) -> None:
        async with self._lock:
            with self.path.open("a") as output:
                output.write(json.dumps(record, ensure_ascii=False) + "\n")
                output.flush()
            self.records[record["sample_id"]] = record

    async def perform(
        self,
        client: AsyncChatClient,
        semaphore: asyncio.Semaphore,
        max_completion_tokens: int,
        solution_continuation_tokens: int,
        verifier_continuation_tokens: int,
        temperature: float,
        top_p: float,
        spec: CallSpec,
        lenient: bool = True,
        stream_detect: bool = False,
        filter_degenerate: bool = True,
        selection_continuation_tokens: int = 2048,
    ) -> dict:
        existing = self.records.get(spec.sample_id)
        if existing is not None:
            if existing["error"] is not None:
                raise RuntimeError(
                    f"persisted failed call {spec.sample_id}: {existing['error']}"
                )
            return existing
        prompt_sha256 = self._save_prompt(spec.messages)
        is_proof_generation = spec.stage.endswith("/generate")
        is_verification = "/verify/" in spec.stage
        is_selection = spec.stage.endswith("/select")
        try:
            async with semaphore:
                if stream_detect and (is_proof_generation or is_verification):
                    # Stream the completion and abort+salvage on a live degenerate
                    # loop (real-time detection). Same record shape as chat_raw.
                    response = await client.chat_stream(
                        spec.messages,
                        max_completion_tokens=max_completion_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        seed=spec.seed,
                        request_id=spec.sample_id,
                        role="solution" if is_proof_generation else "verifier",
                        salvage_max_tokens=(
                            solution_continuation_tokens
                            if is_proof_generation
                            else verifier_continuation_tokens
                        ),
                    )
                else:
                    response = await client.chat_raw(
                        spec.messages,
                        max_completion_tokens=max_completion_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        seed=spec.seed,
                        request_id=spec.sample_id,
                    )
                parser = (
                    parse_generation
                    if is_proof_generation
                    else parse_verification if is_verification else None
                )
                was_length = response["finish_reason"] == "length"
                content = response["message"].get("content") or ""
                xml_valid = False
                xml_error = None
                if parser is not None:
                    try:
                        parser(content, lenient=lenient)
                    except ValueError as error:
                        xml_error = str(error)
                    else:
                        xml_valid = True
                elif is_selection:
                    # "valid" for the parserless selector = a <selected_id> is present.
                    xml_valid = parse_selected_id(content) is not None
                # Length-recovery: force-close the reasoning and continue so a call that
                # rambled to the token budget can still yield its structured answer.
                # Generate/verify re-validate via `parser`; the selector re-checks for a
                # <selected_id>. A parserless, non-selector stage has nothing to recover,
                # so it is skipped (keeps a normal unparseable record, never parser(None)).
                if was_length and not xml_valid and (parser is not None or is_selection):
                    if is_proof_generation:
                        response = await client.continue_solution_raw(
                            response,
                            spec.messages,
                            max_new_tokens=solution_continuation_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            seed=spec.seed,
                            request_id=spec.sample_id,
                        )
                    elif is_verification:
                        response = await client.continue_verification_raw(
                            response,
                            spec.messages,
                            max_new_tokens=verifier_continuation_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            seed=spec.seed,
                            request_id=spec.sample_id,
                        )
                    elif is_selection:
                        response = await client.continue_selection_raw(
                            response,
                            spec.messages,
                            max_new_tokens=selection_continuation_tokens,
                            temperature=temperature,
                            top_p=top_p,
                            seed=spec.seed,
                            request_id=spec.sample_id,
                        )
                    content = response["message"].get("content") or ""
                    if parser is not None:
                        try:
                            parser(content, lenient=lenient)
                        except ValueError as error:
                            xml_valid = False
                            xml_error = str(error)
                        else:
                            xml_valid = True
                            xml_error = None
                    elif is_selection:
                        xml_valid = parse_selected_id(content) is not None
                        xml_error = None if xml_valid else "no <selected_id> after force-close"
                if was_length and xml_valid:
                    response["finish_reason"] = "stop"
                    response["xml_complete_after_length"] = True
                response["xml_valid"] = xml_valid
                response["xml_error"] = xml_error
                if is_verification:
                    # A verifier whose output is a degenerate loop is dropped here (at
                    # disposition time) so mean_score, the _verify_proof filter, AND the
                    # final.json valid/invalid tally all read ONE source of truth (the
                    # disposition) and stay consistent.
                    degenerate = filter_degenerate and is_degenerate(
                        (response["message"].get("reasoning_content") or "")
                        + "\n"
                        + (response["message"].get("content") or "")
                    )
                    if response["finish_reason"] == "stop" and xml_valid and not degenerate:
                        disposition = "accepted"
                    elif not xml_valid:
                        disposition = "skipped_invalid_xml"
                    elif degenerate:
                        disposition = "skipped_degenerate"
                    else:
                        disposition = "skipped_non_stop"
                    response["verification_disposition"] = disposition
            message = response.pop("message")
            record = {
                "sample_id": spec.sample_id,
                "stage": spec.stage,
                "seed": spec.seed,
                "prompt_sha256": prompt_sha256,
                "content": message.get("content") or "",
                "reasoning_content": message.get("reasoning_content") or "",
                **response,
                "error": None,
            }
        except Exception as error:
            record = {
                "sample_id": spec.sample_id,
                "stage": spec.stage,
                "seed": spec.seed,
                "prompt_sha256": prompt_sha256,
                "error": repr(error),
            }
            await self._append(record)
            raise
        await self._append(record)
        return record


class ProblemSearch:
    def __init__(
        self,
        *,
        problem_id: str,
        problem: str,
        output_dir: Path,
        client: AsyncChatClient,
        semaphore: asyncio.Semaphore,
        config: dict,
        on_round_complete: Callable[[dict], Awaitable[None]] | None = None,
    ):
        self.problem_id = problem_id
        self.problem = problem
        self.root = output_dir
        self.client = client
        self.semaphore = semaphore
        self.config = config
        self.on_round_complete = on_round_complete
        self.calls = CallStore(output_dir)
        self.proofs_dir = output_dir / "proofs"
        self.rounds_dir = output_dir / "rounds"
        self.proofs_dir.mkdir(parents=True, exist_ok=True)
        self.rounds_dir.mkdir(parents=True, exist_ok=True)
        self.proofs: dict[str, Proof] = {
            path.stem: Proof.from_dict(json.loads(path.read_text()))
            for path in self.proofs_dir.glob("*.json")
        }

    def _proof_path(self, proof_id: str) -> Path:
        return self.proofs_dir / f"{proof_id}.json"

    def _save_proof(self, proof: Proof) -> None:
        atomic_json(self._proof_path(proof.proof_id), proof.to_dict())
        self.proofs[proof.proof_id] = proof

    def _spec(
        self,
        sample_id: str,
        stage: str,
        messages: list[dict[str, str]],
    ) -> CallSpec:
        return CallSpec(
            sample_id=sample_id,
            stage=stage,
            messages=messages,
            seed=stable_seed(self.config["seed"], self.problem_id, sample_id),
        )

    async def _perform(self, spec: CallSpec, temperature: float | None = None) -> dict:
        # The selector gets its own (smaller) reasoning budget; a ballot that rambles to
        # it is force-closed (</think> + <selected_id>) and continued so it still votes,
        # instead of burning the full max_completion_tokens and returning a null ballot.
        is_selection = spec.stage.endswith("/select")
        max_completion_tokens = (
            int(self.config.get("selection_max_tokens", self.config["max_completion_tokens"]))
            if is_selection
            else self.config["max_completion_tokens"]
        )
        return await self.calls.perform(
            self.client,
            self.semaphore,
            max_completion_tokens,
            self.config["solution_continuation_tokens"],
            self.config["verifier_continuation_tokens"],
            self.config["temperature"] if temperature is None else temperature,
            self.config["top_p"],
            spec,
            lenient=self.config.get("lenient_parsing", True),
            stream_detect=self.config.get("stream_detect", False),
            filter_degenerate=self.config.get("filter_degenerate", True),
            selection_continuation_tokens=int(
                self.config.get("selection_continuation_tokens", 2048)
            ),
        )

    def _rank_key(self, proof: Proof) -> tuple[float, int, float, int]:
        tie = stable_seed(self.config["seed"], self.problem_id, "tie", proof.proof_id)
        return proof.mean_score, len(proof.verifications), proof.self_score, tie

    def ranked(self) -> list[Proof]:
        required = self.config["min_valid_verifications"]
        verified = [
            proof
            for proof in self.proofs.values()
            if len(proof.verifications) >= required
        ]
        return sorted(verified, key=self._rank_key, reverse=True)

    async def _select_final(self, ranked: list[Proof]) -> dict | None:
        """ycchen-style LLM final selector with shuffled-ballot majority voting.

        Each of ``selection_votes`` voters sees the top ``selection_candidates`` proofs in an
        INDEPENDENTLY shuffled order under fresh display IDs (P1, P2, ...), picks one via
        ``<selected_id>`` at low temperature, and we majority-vote the CANONICAL proof_ids
        (so position/label bias is averaged out). Returns the vote breakdown, or None when
        there is nothing to choose or no valid ballot — in which case solve() keeps
        ranked[0] (the current verifier-score behaviour). Selector-call failures degrade
        to a null ballot; they never abort the run.
        """
        votes_n = int(self.config.get("selection_votes", 16))
        # The selector model was only trained to re-rank a SMALL set (ycchen's regime
        # is ~4); feeding it top_proofs (the refinement pool, e.g. 16) is out of
        # distribution. Cap at selection_candidates, decoupled from top_proofs.
        n_cand = int(self.config.get("selection_candidates", 4))
        if len(ranked) < 2:
            return None
        if self.config.get("selection_tournament", False):
            # Tiered selection (see eval_config OPTIONAL_SEARCH_KEYS). When the verifier
            # saturates -- MORE than n_cand proofs tied near its ceiling -- a single
            # top-n_cand re-rank is quality-blind, so play a stratified tournament over the
            # whole saturated band instead. Otherwise fall through to the majority vote, but
            # only over proofs within selection_score_window of the best verifier score, so
            # a 1.0 is never pitted against a 0.3.
            threshold = float(self.config.get("selection_tournament_threshold", 0.95))
            strong = [p for p in ranked if p.mean_score >= threshold]
            if len(strong) > n_cand:
                cap = int(self.config.get("selection_tournament_max_candidates", 10))
                return await self._select_tournament(strong[:cap])
            window = float(self.config.get("selection_score_window", 0.2))
            floor = ranked[0].mean_score * (1.0 - window)
            candidates = [p for p in ranked if p.mean_score >= floor][:n_cand]
        else:
            candidates = ranked[:n_cand]
        if votes_n < 1 or len(candidates) < 2:
            return None
        rank_order = [p.proof_id for p in candidates]

        async def _one_vote(i: int) -> str | None:
            rng = random.Random(
                stable_seed(self.config["seed"], self.problem_id, "select-shuffle", str(i))
            )
            order = list(candidates)
            rng.shuffle(order)
            id_map = {f"P{j + 1}": p.proof_id for j, p in enumerate(order)}
            bundle = selection_bundle(
                [(f"P{j + 1}", p.proof) for j, p in enumerate(order)]
            )
            spec = self._spec(
                f"round-final/select/s{i:02d}",
                "round-final/select",
                selector_messages(self.problem, bundle),
            )
            try:
                record = await self._perform(spec, temperature=SELECTION_TEMPERATURE)
            except Exception:  # a broken selector ballot must not kill the run
                return None
            return id_map.get(parse_selected_id(record.get("content") or ""))

        votes = list(await asyncio.gather(*(_one_vote(i) for i in range(votes_n))))
        winner_id = majority_winner(votes, rank_order)
        if winner_id is None:
            return None
        counts = Counter(v for v in votes if v is not None)
        return {
            "winner_id": winner_id,
            "votes": votes,
            "counts": dict(counts),
            "valid_votes": sum(1 for v in votes if v is not None),
            "total_votes": votes_n,
            "mode": "vote",
        }

    async def _select_tournament(self, pool: list[Proof]) -> dict | None:
        """Stratified tournament over a saturated finalist pool.

        The verifier can't separate proofs once several tie at its ceiling, so instead of
        one top-n re-rank we play ``selection_tournament_rounds`` brackets: each bracket
        pits ``selection_candidates`` proofs (the count the selector prompt is trained for),
        picked so every candidate appears in a balanced number of brackets (stratified, with
        slots shuffled to kill position bias), and we submit the proof that wins the most
        brackets. Ties in wins break toward the better verifier rank. A dead selector call
        drops that bracket to a null result; it never aborts the run.
        """
        rounds_n = int(self.config.get("selection_tournament_rounds", 64))
        group = min(int(self.config.get("selection_candidates", 4)), len(pool))
        if rounds_n < 1 or group < 2 or len(pool) < 2:
            return None
        rank_order = [p.proof_id for p in pool]

        # Stratified brackets: greedily fill each with the least-used candidates (seeded
        # jitter breaks ties) so appearances stay balanced across the pool, then shuffle
        # within the bracket to debias slot position.
        seed_rng = random.Random(
            stable_seed(self.config["seed"], self.problem_id, "select-tournament")
        )
        appearances = {p.proof_id: 0 for p in pool}
        brackets: list[list[Proof]] = []
        for _ in range(rounds_n):
            order = sorted(pool, key=lambda p: (appearances[p.proof_id], seed_rng.random()))
            bracket = order[:group]
            for p in bracket:
                appearances[p.proof_id] += 1
            seed_rng.shuffle(bracket)
            brackets.append(bracket)

        async def _one_round(i: int, bracket: list[Proof]) -> str | None:
            id_map = {f"P{j + 1}": p.proof_id for j, p in enumerate(bracket)}
            bundle = selection_bundle(
                [(f"P{j + 1}", p.proof) for j, p in enumerate(bracket)]
            )
            spec = self._spec(
                f"round-final/select/t{i:03d}",
                "round-final/select",
                selector_messages(self.problem, bundle),
            )
            try:
                record = await self._perform(spec, temperature=SELECTION_TEMPERATURE)
            except Exception:  # a broken bracket must not kill the run
                return None
            return id_map.get(parse_selected_id(record.get("content") or ""))

        wins = list(
            await asyncio.gather(*(_one_round(i, b) for i, b in enumerate(brackets)))
        )
        counts = Counter(w for w in wins if w is not None)
        if not counts:
            return None
        # most wins; ties -> better verifier rank (earlier in the rank-sorted pool)
        winner_id = max(
            rank_order, key=lambda pid: (counts.get(pid, 0), -rank_order.index(pid))
        )
        return {
            "winner_id": winner_id,
            "votes": wins,
            "counts": dict(counts),
            "valid_votes": sum(1 for w in wins if w is not None),
            "total_votes": rounds_n,
            "appearances": appearances,
            "mode": "tournament",
        }

    async def _emit_round_checkpoint(self, summary: dict) -> None:
        if self.on_round_complete is None:
            return
        winner = self.proofs.get(summary["best_proof_id"])
        if winner is None:
            raise RuntimeError(
                "missing checkpoint proof " + summary["best_proof_id"]
            )
        await self.on_round_complete(
            {
                "round": summary["round"],
                "selected_proof_id": winner.proof_id,
                "proof": winner.proof,
                "mean_verifier_score": winner.mean_score,
                "valid_verification_count": len(winner.verifications),
            }
        )

    def _stratified_parents(
        self,
        pool: list[Proof],
        parents_per_call: int,
        n_calls: int,
        round_index: int,
    ) -> list[list[Proof]]:
        """Assign `parents_per_call` distinct parents to each of `n_calls` refine
        calls, drawn from `pool`, so every pool member is used ~equally (stratified)
        and never over- or under-represented. Deterministic: a seeded permutation of
        the pool, then a rotating window -- so the parents are pseudo-random but the
        coverage is even and reproducible."""
        size = len(pool)
        order = sorted(
            range(size),
            key=lambda idx: stable_seed(
                self.config["seed"],
                self.problem_id,
                f"refine-parents-round-{round_index}",
                pool[idx].proof_id,
            ),
        )
        shuffled = [pool[k] for k in order]
        groups: list[list[Proof]] = []
        for call in range(n_calls):
            base = (call * parents_per_call) % size
            # parents_per_call <= size, so these indices are distinct within a call
            groups.append(
                [shuffled[(base + j) % size] for j in range(parents_per_call)]
            )
        return groups

    def _select_reviews(
        self,
        proof: Proof,
        limit: int,
        round_index: int,
        call_index: int,
        strategy: str,
    ) -> list[Verification]:
        """Up to `limit` of the proof's reviews for a refine bundle.

        strategy "worst" (Geremie's original): the lowest-scoring reviews,
        deterministic (score, then seeded tie-break). May include ideal (score 1)
        reviews when the proof has fewer than `limit` non-ideal ones. The same
        parent contributes the same worst reviews to every call it appears in.

        strategy "random_nonideal" (default): a seeded random sample of the
        non-ideal (score < 1) reviews, varied per call; fewer than `limit` if the
        proof has fewer non-ideal reviews, empty if every review scored 1.
        """
        if strategy == "worst":
            ranked = sorted(
                proof.verifications,
                key=lambda v: (
                    v.score,
                    stable_seed(
                        self.config["seed"],
                        self.problem_id,
                        proof.proof_id,
                        f"refine-worst-round-{round_index}",
                        v.sample_id,
                    ),
                ),
            )
            return ranked[:limit]
        nonideal = [v for v in proof.verifications if v.score < 1.0]
        order = sorted(
            range(len(nonideal)),
            key=lambda idx: stable_seed(
                self.config["seed"],
                self.problem_id,
                proof.proof_id,
                f"refine-reviews-round-{round_index}-call-{call_index}",
                nonideal[idx].sample_id,
            ),
        )
        return [nonideal[k] for k in order[:limit]]

    def _round_candidates(self, round_index: int) -> list[Candidate]:
        stage = f"round-{round_index:02d}/generate"
        candidates: list[Candidate] = []
        if round_index == 1:
            messages = generation_messages(self.problem)
            for index in range(self.config["proofs_per_round"]):
                proof_id = f"r{round_index:02d}-p{index:04d}"
                candidates.append(
                    Candidate(
                        proof_id=proof_id,
                        round_index=round_index,
                        parent_id=None,
                        generation=self._spec(
                            f"{stage}/{proof_id}", stage, messages
                        ),
                    )
                )
        else:
            # Pool of refinement parents: the top-ranked verified proofs from
            # earlier rounds (cumulative). Each refine call merges refine_parents
            # of them (stratified for even coverage), each contributing up to
            # reviews_per_refine_parent random non-ideal reviews.
            pool = [
                proof
                for proof in self.ranked()
                if proof.round_index < round_index
            ][: self.config["top_proofs"]]
            if not pool:
                raise RuntimeError(f"{self.problem_id} has no verified proof to refine")
            # Gold drops the prover self-evaluation from the refiner bundle
            # (v2/pool_loop.py: with_self_eval=False, "unreliable ~92% self-score 1").
            refiner_self_eval = self.config.get("refiner_sees_self_evaluation", False)
            n_calls = self.config["proofs_per_round"]  # keep round width
            parents_per_call = min(self.config["refine_parents"], len(pool))
            reviews_per_parent = self.config["reviews_per_refine_parent"]
            review_strategy = self.config.get(
                "refine_review_strategy", "random_nonideal"
            )
            groups = self._stratified_parents(
                pool, parents_per_call, n_calls, round_index
            )
            for call_index in range(n_calls):
                proof_id = f"r{round_index:02d}-p{call_index:04d}"
                bundle = [
                    (
                        parent.proof_id,
                        parent.proof,
                        parent.self_evaluation if refiner_self_eval else "",
                        [
                            (review.score, review.analysis)
                            for review in self._select_reviews(
                                parent,
                                reviews_per_parent,
                                round_index,
                                call_index,
                                review_strategy,
                            )
                        ],
                    )
                    for parent in groups[call_index]
                ]
                messages = refinement_messages(self.problem, bundle)
                candidates.append(
                    Candidate(
                        proof_id=proof_id,
                        round_index=round_index,
                        # multi-parent ancestry (audit only), comma-joined
                        parent_id=",".join(parent.proof_id for parent in groups[call_index]),
                        generation=self._spec(
                            f"{stage}/{proof_id}", stage, messages
                        ),
                    )
                )
        return candidates

    def _admit_candidate(self, candidate: Candidate, record: dict) -> Proof | None:
        if candidate.proof_id in self.proofs:
            return self.proofs[candidate.proof_id]
        if record["finish_reason"] != "stop":
            return None
        # Reject degenerate (looping) generations: a proof that fell into a
        # repetition/enumeration loop and stopped at the token cap must not enter
        # the pool or seed refinements. gzip-based, so distribution-neutral (see
        # loop_detect); truncated loops are already dropped by the check above.
        # Gated by search.filter_degenerate (default on).
        if self.config.get("filter_degenerate", True) and is_degenerate(
            (record.get("reasoning_content") or "") + "\n" + (record.get("content") or "")
        ):
            return None
        try:
            proof_text, self_evaluation, self_score = parse_generation(
                record["content"],
                lenient=self.config.get("lenient_parsing", True),
            )
        except ValueError:
            return None
        proof = Proof(
            proof_id=candidate.proof_id,
            round_index=candidate.round_index,
            parent_id=candidate.parent_id,
            proof=proof_text,
            self_evaluation=self_evaluation,
            self_score=self_score,
            generation_sample_id=record["sample_id"],
        )
        self._save_proof(proof)
        return proof

    async def _verify_proof(self, proof: Proof) -> dict:
        stage = f"round-{proof.round_index:02d}/verify/{proof.proof_id}"
        # The verifier was trained with the candidate's self-evaluation in its
        # prompt (training/opd_v2 build_verify passes proof.self_eval), so the
        # default feeds it. Setting verifier_sees_self_evaluation=false blanks it
        # to test the anchoring hypothesis -- but that prompt shape is off the
        # verifier's training distribution.
        self_evaluation = (
            proof.self_evaluation
            if self.config.get("verifier_sees_self_evaluation", True)
            else ""
        )
        messages = verification_messages(
            self.problem,
            proof.proof,
            self_evaluation,
        )
        specs = [
            self._spec(f"{stage}/v{index:03d}", stage, messages)
            for index in range(self.config["verifications_per_proof"])
        ]
        records = await asyncio.gather(
            *(self._perform(spec) for spec in specs)
        )
        verifications: list[Verification] = []
        invalid_sample_ids: list[str] = []
        for spec, record in zip(specs, records, strict=True):
            # Any disposition other than 'accepted' is dropped -- including
            # 'skipped_degenerate' (set in perform when filter_degenerate is on), so
            # mean_score AND the final.json valid/invalid tally read the same source
            # and stay consistent. A dropped verification's score must not pollute
            # mean_score.
            if record["verification_disposition"] != "accepted":
                invalid_sample_ids.append(spec.sample_id)
                continue
            analysis, score = parse_verification(
                record["content"],
                lenient=self.config.get("lenient_parsing", True),
            )
            verifications.append(
                Verification(
                    sample_id=spec.sample_id,
                    score=score,
                    analysis=analysis,
                )
            )
        proof.verifications = verifications
        self._save_proof(proof)
        return {
            "attempted": len(specs),
            "valid": len(verifications),
            "invalid": len(invalid_sample_ids),
            "invalid_sample_ids": invalid_sample_ids,
        }

    async def _complete_candidate(
        self,
        candidate: Candidate,
        generation_task: asyncio.Task[dict],
    ) -> tuple[Proof | None, dict | None]:
        record = await generation_task
        proof = self._admit_candidate(candidate, record)
        if proof is None:
            return None, None
        return proof, await self._verify_proof(proof)

    async def _run_round(self, round_index: int) -> tuple[list[Proof], dict]:
        candidates = self._round_candidates(round_index)
        generation_tasks = [
            asyncio.create_task(self._perform(candidate.generation))
            for candidate in candidates
        ]
        results = await asyncio.gather(
            *(
                self._complete_candidate(candidate, generation_task)
                for candidate, generation_task in zip(
                    candidates, generation_tasks, strict=True
                )
            )
        )
        generated: list[Proof] = []
        stats = {
            "attempted": 0,
            "valid": 0,
            "invalid": 0,
            "by_proof": {},
        }
        for proof, proof_stats in results:
            if proof is None or proof_stats is None:
                continue
            generated.append(proof)
            stats["attempted"] += proof_stats["attempted"]
            stats["valid"] += proof_stats["valid"]
            stats["invalid"] += proof_stats["invalid"]
            stats["by_proof"][proof.proof_id] = proof_stats
        if not generated:
            raise RuntimeError(
                f"{self.problem_id} round {round_index} produced no valid proof"
            )
        return generated, stats

    def _round_summary(
        self,
        round_index: int,
        generated: list[Proof],
        verification_stats: dict,
    ) -> dict:
        ranked = self.ranked()
        if not ranked:
            minimum = self.config["min_valid_verifications"]
            raise RuntimeError(
                f"{self.problem_id} round {round_index} produced no proof with "
                f"at least {minimum} valid verifications"
            )
        return {
            "schema_version": 2,
            "problem_id": self.problem_id,
            "round": round_index,
            "generated_proof_ids": [proof.proof_id for proof in generated],
            "cumulative_pool_size": len(self.proofs),
            "verified_pool_size": len(ranked),
            "best_proof_id": ranked[0].proof_id,
            "best_mean_score": ranked[0].mean_score,
            "best_valid_verification_count": len(ranked[0].verifications),
            "verification_stats": verification_stats,
            "early_stop": ranked[0].mean_score
            > self.config["early_stop_threshold"],
        }

    async def solve(self) -> dict:
        final_path = self.root / "final.json"
        if final_path.exists():
            return json.loads(final_path.read_text())
        completed_summaries = {
            int(path.stem.split("-")[-1]): json.loads(path.read_text())
            for path in self.rounds_dir.glob("round-*.json")
        }
        if completed_summaries:
            latest_round = max(completed_summaries)
            await self._emit_round_checkpoint(
                completed_summaries[latest_round]
            )
        for round_index in range(1, self.config["max_rounds"] + 1):
            if round_index in completed_summaries:
                if completed_summaries[round_index]["early_stop"]:
                    break
                continue
            generated, verification_stats = await self._run_round(round_index)
            summary = self._round_summary(
                round_index, generated, verification_stats
            )
            atomic_json(self.rounds_dir / f"round-{round_index:02d}.json", summary)
            await self._emit_round_checkpoint(summary)
            if summary["early_stop"]:
                break

        ranked = self.ranked()
        if not ranked:
            minimum = self.config["min_valid_verifications"]
            raise RuntimeError(
                f"{self.problem_id} has no proof with at least "
                f"{minimum} valid verifications"
            )
        winner = ranked[0]
        final_source = "verification_pool"
        selection = None
        if self.config.get("llm_selector", False):
            selection = await self._select_final(ranked)
            if selection is not None:
                chosen = self.proofs.get(selection["winner_id"])
                if chosen is not None:
                    winner = chosen
                    mode = selection.get("mode", "vote")
                    tag = "llm_selector" if mode == "vote" else f"llm_selector[{mode}]"
                    final_source = (
                        f"{tag}:{selection['winner_id']}("
                        f"{selection['counts'].get(selection['winner_id'], 0)}/"
                        f"{selection['total_votes']})"
                    )
        verification_records = [
            record
            for record in self.calls.records.values()
            if "/verify/" in record["stage"] and record["error"] is None
        ]
        final = {
            "schema_version": 2,
            "problem_id": self.problem_id,
            "final_source": final_source,
            "selected_proof_id": winner.proof_id,
            "final_proof": winner.proof,
            "mean_verifier_score": winner.mean_score,
            "valid_verification_count": len(winner.verifications),
            "self_score": winner.self_score,
            "rounds_completed": len(list(self.rounds_dir.glob("round-*.json"))),
            "proofs_in_pool": len(self.proofs),
            "calls_completed": len(self.calls.records),
            "physical_requests_completed": sum(
                record.get("physical_request_count", 1)
                for record in self.calls.records.values()
            ),
            "valid_verifications_completed": sum(
                record.get("verification_disposition") == "accepted"
                for record in verification_records
            ),
            "invalid_verifications_completed": sum(
                record.get("verification_disposition") != "accepted"
                for record in verification_records
            ),
        }
        if selection is not None:
            final["selection"] = selection
        atomic_json(final_path, final)
        return final
