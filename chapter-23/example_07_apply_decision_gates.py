"""Select an evidence-proportional action from explicit decision gates."""

from __future__ import annotations


GATES: tuple[tuple[str, frozenset[str]], ...] = (
    ("monitor", frozenset({"problem_contract", "source_register"})),
    (
        "reproduce",
        frozenset(
            {
                "problem_contract",
                "source_register",
                "artifacts",
                "environment",
                "validator",
            }
        ),
    ),
    (
        "explore",
        frozenset(
            {
                "problem_contract",
                "classical_baseline",
                "artifacts",
                "validator",
                "limitations",
            }
        ),
    ),
    (
        "pilot",
        frozenset(
            {
                "problem_contract",
                "classical_baseline",
                "quantum_evidence",
                "resource_account",
                "user_outcome",
                "security_review",
                "owner",
                "stop_conditions",
            }
        ),
    ),
)


def eligible_actions(records: set[str]) -> list[str]:
    return [name for name, required in GATES if required <= records]


records = {
    "problem_contract",
    "source_register",
    "classical_baseline",
    "artifacts",
    "environment",
    "validator",
    "limitations",
}
actions = eligible_actions(records)
assert actions == ["monitor", "reproduce", "explore"]
assert "pilot" not in actions
print("eligible actions:", actions)
print("current decision: explore for learning; do not infer pilot readiness")
