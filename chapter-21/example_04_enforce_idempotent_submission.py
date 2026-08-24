"""Return one service job for repeated requests with the same semantic input."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


def request_digest(request: dict[str, object]) -> str:
    payload = json.dumps(request, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class IdempotencyConflict(ValueError):
    pass


@dataclass(frozen=True)
class Submission:
    job_id: str
    request_hash: str


class SubmissionStore:
    def __init__(self) -> None:
        self._by_key: dict[str, Submission] = {}

    def submit(self, key: str, request: dict[str, object]) -> tuple[Submission, bool]:
        digest = request_digest(request)
        existing = self._by_key.get(key)
        if existing is not None:
            if existing.request_hash != digest:
                raise IdempotencyConflict("the key was reused with different input")
            return existing, False

        submission = Submission(
            job_id=f"job-{len(self._by_key) + 1:04d}",
            request_hash=digest,
        )
        self._by_key[key] = submission
        return submission, True


store = SubmissionStore()
request = {"intent_hash": "intent-a", "shots": 1024, "backend": "target-a"}

first, first_created = store.submit("client-key-7", request)
second, second_created = store.submit("client-key-7", dict(request))
assert first == second
assert first_created is True and second_created is False

try:
    store.submit("client-key-7", {**request, "shots": 2048})
except IdempotencyConflict as error:
    print(error)

print(first.job_id, second.job_id, len(store._by_key))
