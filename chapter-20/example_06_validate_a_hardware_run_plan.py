"""Validate a hardware run plan without authenticating or submitting a job."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json


@dataclass(frozen=True)
class IntentRecord:
    experiment_id: str
    qubits: int
    shots: int
    required_operations: tuple[str, ...]
    measurement: str


@dataclass(frozen=True)
class CapabilityRecord:
    provider: str
    backend_name: str
    checked_at: str
    operational: bool
    num_qubits: int
    supported_operations: tuple[str, ...]
    max_shots: int


intent = IntentRecord(
    experiment_id="bell-parity-001",
    qubits=2,
    shots=2048,
    required_operations=("rz", "sx", "x", "cz", "measure"),
    measurement="computational-basis bitstrings",
)
capability = CapabilityRecord(
    provider="provider-name-from-live-query",
    backend_name="backend-name-from-live-query",
    checked_at=datetime.now(timezone.utc).isoformat(),
    operational=True,
    num_qubits=5,
    supported_operations=("rz", "sx", "x", "cz", "measure"),
    max_shots=100_000,
)

errors = []
if not capability.operational:
    errors.append("backend is not operational")
if intent.qubits > capability.num_qubits:
    errors.append("intent requires more qubits than the backend exposes")
if intent.shots > capability.max_shots:
    errors.append("shot request exceeds the recorded backend limit")
missing = set(intent.required_operations) - set(capability.supported_operations)
if missing:
    errors.append(f"unsupported operations: {sorted(missing)}")

plan = {
    "intent": asdict(intent),
    "capability": asdict(capability),
    "validation_errors": errors,
    "authorization": "not granted by this script",
    "submission_status": "READY_FOR_REVIEW_NOT_SUBMITTED" if not errors else "BLOCKED",
}

print(json.dumps(plan, indent=2))
assert plan["submission_status"] == "READY_FOR_REVIEW_NOT_SUBMITTED"

