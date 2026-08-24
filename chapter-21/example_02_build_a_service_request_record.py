"""Build a stable service request without embedding provider credentials."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExperimentIntent:
    circuit_family: str
    qubits: int
    measurement: str
    shots: int

    def validate(self) -> None:
        if self.qubits < 1:
            raise ValueError("qubits must be positive")
        if self.shots < 1:
            raise ValueError("shots must be positive")
        if self.measurement not in {"counts", "expectation"}:
            raise ValueError("unsupported measurement contract")


@dataclass(frozen=True)
class ServiceRequest:
    request_id: str
    tenant_ref: str
    idempotency_key: str
    intent_hash: str
    backend_selector: str
    created_at: str


def build_request(
    *,
    request_id: str,
    tenant_ref: str,
    idempotency_key: str,
    intent: ExperimentIntent,
    backend_selector: str,
    created_at: str,
) -> ServiceRequest:
    intent.validate()
    if not idempotency_key.strip():
        raise ValueError("idempotency_key is required")
    return ServiceRequest(
        request_id=request_id,
        tenant_ref=tenant_ref,
        idempotency_key=idempotency_key,
        intent_hash=canonical_digest(asdict(intent)),
        backend_selector=backend_selector,
        created_at=created_at,
    )


intent = ExperimentIntent(
    circuit_family="bell-parity",
    qubits=2,
    measurement="counts",
    shots=1024,
)
request = build_request(
    request_id="req-0001",
    tenant_ref="tenant-a",
    idempotency_key="training-request-0001",
    intent=intent,
    backend_selector="least-busy-compatible-target",
    created_at="2026-08-22T00:00:00Z",
)

record = asdict(request)
assert "token" not in record and "password" not in record
print(json.dumps(record, indent=2, sort_keys=True))
