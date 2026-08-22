"""Validate pedagogical unit-commitment candidates independently of a solver."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Generator:
    name: str
    output_when_on: int
    cost_when_on: int


GENERATORS = (
    Generator("north", output_when_on=4, cost_when_on=7),
    Generator("central", output_when_on=3, cost_when_on=5),
    Generator("south", output_when_on=2, cost_when_on=4),
)
DEMAND = (5, 7, 6)


def validate_schedule(schedule: tuple[tuple[int, ...], ...]) -> dict[str, object]:
    violations: list[str] = []
    if len(schedule) != len(DEMAND):
        return {"feasible": False, "violations": ["wrong number of periods"]}

    total_cost = 0
    supplied: list[int] = []
    for period, (row, demand) in enumerate(zip(schedule, DEMAND)):
        if len(row) != len(GENERATORS) or set(row) - {0, 1}:
            violations.append(f"period {period}: invalid binary decisions")
            continue
        output = sum(bit * unit.output_when_on for bit, unit in zip(row, GENERATORS))
        cost = sum(bit * unit.cost_when_on for bit, unit in zip(row, GENERATORS))
        supplied.append(output)
        total_cost += cost
        if output < demand:
            violations.append(f"period {period}: supply {output} below demand {demand}")

    return {
        "feasible": not violations,
        "violations": violations,
        "supplied": supplied,
        "cost_units": total_cost,
        "model_scope": "pedagogical fixed-output commitment only",
    }


candidate_a = ((1, 1, 0), (1, 1, 0), (1, 0, 1))
candidate_b = ((0, 1, 1), (1, 0, 1), (0, 1, 1))
result_a = validate_schedule(candidate_a)
result_b = validate_schedule(candidate_b)

assert result_a["feasible"] is True
assert result_b["feasible"] is False
print("candidate_a:", result_a)
print("candidate_b:", result_b)
