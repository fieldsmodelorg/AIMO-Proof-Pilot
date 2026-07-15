"""YAML-driven generate-verify-refine proof-pool search."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any

from async_client import AsyncChatClient
from proof_prompts import (
    generation_messages,
    parse_generation,
    parse_verification,
    refinement_messages,
    verification_messages,
)


def stable_seed(base: int, *parts: str) -> int:
    material = "\0".join([str(base), *parts]).encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big") % (2**31 - 1)


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
    ) -> dict:
        existing = self.records.get(spec.sample_id)
        if existing is not None:
            if existing["error"] is not None:
                raise RuntimeError(
                    f"persisted failed call {spec.sample_id}: {existing['error']}"
                )
            return existing
        prompt_sha256 = self._save_prompt(spec.messages)
        try:
            async with semaphore:
                response = await client.chat_raw(
                    spec.messages,
                    max_completion_tokens=max_completion_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    seed=spec.seed,
                    request_id=spec.sample_id,
                )
                is_proof_generation = spec.stage.endswith("/generate")
                is_verification = "/verify/" in spec.stage
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
                        parser(content)
                    except ValueError as error:
                        xml_error = str(error)
                    else:
                        xml_valid = True
                if was_length and not xml_valid:
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
                    content = response["message"].get("content") or ""
                    try:
                        parser(content)
                    except ValueError as error:
                        xml_valid = False
                        xml_error = str(error)
                    else:
                        xml_valid = True
                        xml_error = None
                if was_length and xml_valid:
                    response["finish_reason"] = "stop"
                    response["xml_complete_after_length"] = True
                response["xml_valid"] = xml_valid
                response["xml_error"] = xml_error
                if is_verification:
                    if response["finish_reason"] == "stop" and xml_valid:
                        disposition = "accepted"
                    elif not xml_valid:
                        disposition = "skipped_invalid_xml"
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

    async def _perform(self, spec: CallSpec) -> dict:
        return await self.calls.perform(
            self.client,
            self.semaphore,
            self.config["max_completion_tokens"],
            self.config["solution_continuation_tokens"],
            self.config["verifier_continuation_tokens"],
            self.config["temperature"],
            self.config["top_p"],
            spec,
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

    def _selected_reviews(
        self,
        proof: Proof,
        round_index: int,
    ) -> list[Verification]:
        limit = self.config["analyses_per_refinement"]
        ranked = sorted(
            proof.verifications,
            key=lambda verification: (
                verification.score,
                stable_seed(
                    self.config["seed"],
                    self.problem_id,
                    proof.proof_id,
                    f"round-{round_index}",
                    verification.sample_id,
                ),
            ),
        )
        return ranked[:limit]

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
            parents = [
                proof
                for proof in self.ranked()
                if proof.round_index < round_index
            ][: self.config["top_proofs"]]
            if not parents:
                raise RuntimeError(f"{self.problem_id} has no verified proof to refine")
            proof_index = 0
            for parent in parents:
                reviews = self._selected_reviews(parent, round_index)
                if len(reviews) != self.config["analyses_per_refinement"]:
                    raise RuntimeError(
                        f"{parent.proof_id} has too few verifier analyses to refine"
                    )
                for review in reviews:
                    proof_id = f"r{round_index:02d}-p{proof_index:04d}"
                    messages = refinement_messages(
                        self.problem,
                        parent.proof_id,
                        parent.proof,
                        parent.self_evaluation,
                        review.score,
                        review.analysis,
                    )
                    candidates.append(
                        Candidate(
                            proof_id=proof_id,
                            round_index=round_index,
                            parent_id=parent.proof_id,
                            generation=self._spec(
                                f"{stage}/{proof_id}", stage, messages
                            ),
                        )
                    )
                    proof_index += 1
        return candidates

    def _admit_candidate(self, candidate: Candidate, record: dict) -> Proof | None:
        if candidate.proof_id in self.proofs:
            return self.proofs[candidate.proof_id]
        if record["finish_reason"] != "stop":
            return None
        try:
            proof_text, self_evaluation, self_score = parse_generation(
                record["content"]
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
        messages = verification_messages(
            self.problem,
            proof.proof,
            proof.self_evaluation,
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
            if record["verification_disposition"] != "accepted":
                invalid_sample_ids.append(spec.sample_id)
                continue
            analysis, score = parse_verification(record["content"])
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
        verification_records = [
            record
            for record in self.calls.records.values()
            if "/verify/" in record["stage"] and record["error"] is None
        ]
        final = {
            "schema_version": 2,
            "problem_id": self.problem_id,
            "final_source": "verification_pool",
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
        atomic_json(final_path, final)
        return final
