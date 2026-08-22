"""Aggregate service metrics without using job or user identifiers as labels."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from statistics import fmean


FORBIDDEN_LABELS = {"job_id", "request_id", "tenant_id", "user_id"}


@dataclass
class ServiceMetrics:
    outcomes: Counter[str] = field(default_factory=Counter)
    submission_seconds: list[float] = field(default_factory=list)
    execution_seconds: list[float] = field(default_factory=list)
    cache_lookups: int = 0
    cache_hits: int = 0

    def observe_job(
        self,
        *,
        outcome: str,
        submission_seconds: float,
        execution_seconds: float,
        labels: dict[str, str],
    ) -> None:
        forbidden = FORBIDDEN_LABELS.intersection(labels)
        if forbidden:
            raise ValueError(f"high-cardinality labels rejected: {sorted(forbidden)}")
        self.outcomes[outcome] += 1
        self.submission_seconds.append(submission_seconds)
        self.execution_seconds.append(execution_seconds)

    def observe_cache(self, hit: bool) -> None:
        self.cache_lookups += 1
        self.cache_hits += int(hit)

    def summary(self) -> dict[str, object]:
        return {
            "outcomes": dict(sorted(self.outcomes.items())),
            "mean_submission_seconds": round(fmean(self.submission_seconds), 3),
            "mean_execution_seconds": round(fmean(self.execution_seconds), 3),
            "cache_hit_ratio": self.cache_hits / self.cache_lookups,
        }


metrics = ServiceMetrics()
metrics.observe_job(
    outcome="succeeded",
    submission_seconds=0.2,
    execution_seconds=1.4,
    labels={"provider": "local", "evidence_class": "ideal-simulator"},
)
metrics.observe_job(
    outcome="failed",
    submission_seconds=0.4,
    execution_seconds=0.1,
    labels={"provider": "local", "evidence_class": "ideal-simulator"},
)
metrics.observe_cache(True)
metrics.observe_cache(False)
print(metrics.summary())
