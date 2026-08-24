"""Trace nested quantum execution without calling a provider."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class BoundaryEvent:
    boundary: str
    owner: str
    repeated_object: str
    record: str
    scientific_work: bool


def trace_one_algorithm_iteration(shots: int) -> dict[str, object]:
    if shots < 1:
        raise ValueError("shots must be positive")

    scientific_path = (
        BoundaryEvent(
            boundary="python construction",
            owner="application",
            repeated_object="parameter binding",
            record="intent",
            scientific_work=True,
        ),
        BoundaryEvent(
            boundary="compilation",
            owner="compiler",
            repeated_object="candidate target mapping",
            record="plan",
            scientific_work=True,
        ),
        BoundaryEvent(
            boundary="provider job",
            owner="provider adapter",
            repeated_object="approved compiled work",
            record="job",
            scientific_work=True,
        ),
        BoundaryEvent(
            boundary="shot batch",
            owner="execution system",
            repeated_object=f"fresh preparation and Bell-circuit execution × {shots}",
            record="raw result",
            scientific_work=True,
        ),
        BoundaryEvent(
            boundary="classical update",
            owner="domain algorithm",
            repeated_object="estimate to next parameters",
            record="derived result",
            scientific_work=True,
        ),
    )

    operations_path = (
        BoundaryEvent(
            boundary="provider polling",
            owner="service adapter",
            repeated_object="status observation",
            record="job event",
            scientific_work=False,
        ),
        BoundaryEvent(
            boundary="reconciliation",
            owner="orchestrator",
            repeated_object="uncertain submission lookup",
            record="operations",
            scientific_work=False,
        ),
    )

    return {
        "scientific_path": [asdict(event) for event in scientific_path],
        "operations_path": [asdict(event) for event in operations_path],
    }


trace = trace_one_algorithm_iteration(shots=1024)
assert all(event["scientific_work"] for event in trace["scientific_path"])
assert not any(event["scientific_work"] for event in trace["operations_path"])
assert trace["scientific_path"][-1]["boundary"] == "classical update"
print(json.dumps(trace, indent=2, sort_keys=True))
