"""Recover a provider job after a timeout without submitting duplicate work."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderJob:
    provider_job_id: str
    client_token: str
    status: str


class ProviderStub:
    def __init__(self) -> None:
        self.jobs: dict[str, ProviderJob] = {}
        self.calls = 0

    def submit(self, client_token: str) -> ProviderJob:
        self.calls += 1
        existing = self.jobs.get(client_token)
        if existing is not None:
            return existing
        job = ProviderJob("provider-job-0001", client_token, "queued")
        self.jobs[client_token] = job
        raise TimeoutError("connection ended after the provider accepted the job")

    def find_by_client_token(self, client_token: str) -> ProviderJob | None:
        return self.jobs.get(client_token)


def submit_with_reconciliation(provider: ProviderStub, client_token: str) -> ProviderJob:
    try:
        return provider.submit(client_token)
    except TimeoutError:
        recovered = provider.find_by_client_token(client_token)
        if recovered is None:
            raise RuntimeError("submission outcome is unknown; manual reconciliation required")
        return recovered


provider = ProviderStub()
job = submit_with_reconciliation(provider, "client-token-0001")
assert provider.calls == 1
assert len(provider.jobs) == 1
print(job.provider_job_id, job.status, provider.calls)
