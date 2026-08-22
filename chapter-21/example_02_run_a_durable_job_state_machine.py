"""Validate service-job transitions and retain an append-only event history."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class JobState(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    SUBMITTING = "submitting"
    SUBMITTED = "submitted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


ALLOWED: dict[JobState, set[JobState]] = {
    JobState.RECEIVED: {JobState.VALIDATED, JobState.FAILED},
    JobState.VALIDATED: {JobState.SUBMITTING, JobState.CANCELLED},
    JobState.SUBMITTING: {JobState.SUBMITTED, JobState.FAILED},
    JobState.SUBMITTED: {
        JobState.RUNNING,
        JobState.SUCCEEDED,
        JobState.FAILED,
        JobState.CANCELLED,
    },
    JobState.RUNNING: {
        JobState.SUCCEEDED,
        JobState.FAILED,
        JobState.CANCELLED,
    },
    JobState.SUCCEEDED: set(),
    JobState.FAILED: set(),
    JobState.CANCELLED: set(),
}


@dataclass(frozen=True)
class JobEvent:
    sequence: int
    state: JobState
    reason: str


@dataclass
class ServiceJob:
    job_id: str
    state: JobState = JobState.RECEIVED
    events: list[JobEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.events.append(JobEvent(1, self.state, "request accepted"))

    def transition(self, target: JobState, reason: str) -> None:
        if target not in ALLOWED[self.state]:
            raise ValueError(f"invalid transition: {self.state.value} -> {target.value}")
        self.state = target
        self.events.append(JobEvent(len(self.events) + 1, target, reason))


job = ServiceJob("job-0001")
job.transition(JobState.VALIDATED, "policy and capability checks passed")
job.transition(JobState.SUBMITTING, "immutable plan stored")
job.transition(JobState.SUBMITTED, "provider identifier attached")
job.transition(JobState.RUNNING, "provider reports execution")
job.transition(JobState.SUCCEEDED, "raw result stored and validated")

try:
    job.transition(JobState.RUNNING, "terminal jobs cannot restart")
except ValueError as error:
    print(error)

for event in job.events:
    print(event.sequence, event.state.value, event.reason)
