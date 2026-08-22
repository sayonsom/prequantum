"""Normalize provider status for control flow while preserving source metadata."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NormalizedState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


STATUS_MAP: dict[str, dict[str, NormalizedState]] = {
    "ibm": {
        "queued": NormalizedState.QUEUED,
        "running": NormalizedState.RUNNING,
        "completed": NormalizedState.SUCCEEDED,
        "failed": NormalizedState.FAILED,
        "cancelled": NormalizedState.CANCELLED,
    },
    "aws-braket": {
        "QUEUED": NormalizedState.QUEUED,
        "RUNNING": NormalizedState.RUNNING,
        "COMPLETED": NormalizedState.SUCCEEDED,
        "FAILED": NormalizedState.FAILED,
        "CANCELLED": NormalizedState.CANCELLED,
    },
}


@dataclass(frozen=True)
class ProviderJobSnapshot:
    provider: str
    provider_job_id: str
    provider_status: str
    normalized_state: NormalizedState
    observed_at: str
    backend_reference: str | None


def normalize(
    provider: str,
    provider_job_id: str,
    provider_status: str,
    observed_at: str,
    backend_reference: str | None,
) -> ProviderJobSnapshot:
    normalized = STATUS_MAP.get(provider, {}).get(
        provider_status,
        NormalizedState.UNKNOWN,
    )
    return ProviderJobSnapshot(
        provider=provider,
        provider_job_id=provider_job_id,
        provider_status=provider_status,
        normalized_state=normalized,
        observed_at=observed_at,
        backend_reference=backend_reference,
    )


snapshots = [
    normalize("ibm", "ibm-job-7", "completed", "2026-08-22T00:00:00Z", "backend-a"),
    normalize("aws-braket", "braket-job-9", "RUNNING", "2026-08-22T00:00:01Z", "device-b"),
    normalize("provider-c", "job-11", "PAUSED", "2026-08-22T00:00:02Z", None),
]
for snapshot in snapshots:
    print(snapshot.provider, snapshot.provider_status, snapshot.normalized_state.value)
