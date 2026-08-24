"""Cache a result only when every evidence-defining field is identical."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceKey:
    intent_hash: str
    capability_snapshot_id: str
    compilation_hash: str
    execution_mode: str
    shots: int
    run_options_hash: str


@dataclass(frozen=True)
class EvidenceRecord:
    raw_result_ref: str
    created_at: str
    evidence_class: str


class EvidenceCache:
    def __init__(self) -> None:
        self._records: dict[EvidenceKey, EvidenceRecord] = {}

    def put(self, key: EvidenceKey, record: EvidenceRecord) -> None:
        self._records[key] = record

    def get(self, key: EvidenceKey) -> EvidenceRecord | None:
        return self._records.get(key)


key = EvidenceKey(
    intent_hash="intent-a",
    capability_snapshot_id="target-snapshot-17",
    compilation_hash="isa-circuit-31",
    execution_mode="ideal-finite-shot-simulator",
    shots=1024,
    run_options_hash="options-a",
)
record = EvidenceRecord(
    raw_result_ref="results/result-0001.json",
    created_at="2026-08-22T00:00:00Z",
    evidence_class="finite-shot ideal simulation",
)

cache = EvidenceCache()
cache.put(key, record)
assert cache.get(key) == record

changed_shots = EvidenceKey(**{**key.__dict__, "shots": 2048})
assert cache.get(changed_shots) is None
print(cache.get(key))
print(cache.get(changed_shots))
