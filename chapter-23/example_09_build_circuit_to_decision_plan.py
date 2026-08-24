"""Validate a circuit-to-decision plan without inventing an execution result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Boundary:
    name: str
    owner: str
    repeated_object: str
    persistent_record: str


@dataclass(frozen=True)
class CircuitDecisionPlan:
    task: str
    logical_circuit: tuple[str, ...]
    measurement_map: tuple[tuple[str, str], ...]
    shots_per_batch: int
    batches: int
    evidence_type: str
    eligible_action: str
    boundaries: tuple[Boundary, ...]


def validate_plan(plan: CircuitDecisionPlan) -> list[str]:
    errors: list[str] = []
    required_gates = ("H q0", "CNOT q0->q1", "MEASURE q0->c0", "MEASURE q1->c1")
    if plan.logical_circuit != required_gates:
        errors.append("logical circuit or operand order differs from the declared trace")
    if plan.measurement_map != (("q0", "c0"), ("q1", "c1")):
        errors.append("measurement map must preserve q0->c0 and q1->c1")
    if plan.shots_per_batch <= 0 or plan.batches <= 0:
        errors.append("shot and batch counts must be positive")
    if plan.evidence_type == "plan_only" and plan.eligible_action not in {
        "learn",
        "reproduce",
    }:
        errors.append("a plan-only record supports learn or reproduce, not a pilot")

    expected_boundaries = {
        "construction",
        "coherent_execution",
        "shots",
        "experiment_batches",
        "review",
    }
    names = {boundary.name for boundary in plan.boundaries}
    if names != expected_boundaries:
        errors.append("the five repetition boundaries must be recorded separately")
    if len(names) != len(plan.boundaries):
        errors.append("boundary names must be unique")
    if any(not boundary.persistent_record for boundary in plan.boundaries):
        errors.append("every boundary needs a persistent evidence record")
    return errors


plan = CircuitDecisionPlan(
    task="prepare a Bell state and estimate same-bit probability",
    logical_circuit=(
        "H q0",
        "CNOT q0->q1",
        "MEASURE q0->c0",
        "MEASURE q1->c1",
    ),
    measurement_map=(("q0", "c0"), ("q1", "c1")),
    shots_per_batch=1000,
    batches=3,
    evidence_type="plan_only",
    eligible_action="reproduce",
    boundaries=(
        Boundary(
            "construction",
            "Python driver",
            "append one logical circuit",
            "logical-circuit digest",
        ),
        Boundary(
            "coherent_execution",
            "quantum target",
            "H then controlled-X before measurement",
            "scheduled-circuit digest",
        ),
        Boundary(
            "shots",
            "execution service",
            "fresh preparation and measurement",
            "raw counts",
        ),
        Boundary(
            "experiment_batches",
            "experiment driver",
            "one job under a declared context",
            "job and environment manifest",
        ),
        Boundary(
            "review",
            "evidence reviewer",
            "comparison after a trigger",
            "versioned decision record",
        ),
    ),
)

errors = validate_plan(plan)
assert errors == []
assert plan.evidence_type == "plan_only"
print("eligible action:", plan.eligible_action)
for boundary in plan.boundaries:
    print(boundary.name, "->", boundary.persistent_record)
