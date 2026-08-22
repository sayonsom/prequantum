"""Build a portfolio manifest with explicit evidence dependencies."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    kind: str
    digest: str
    depends_on: tuple[str, ...] = ()


def validate_manifest(artifacts: tuple[Artifact, ...]) -> list[str]:
    identifiers = {artifact.artifact_id for artifact in artifacts}
    if len(identifiers) != len(artifacts):
        return ["artifact identifiers must be unique"]
    errors: list[str] = []
    for artifact in artifacts:
        for dependency in artifact.depends_on:
            if dependency not in identifiers:
                errors.append(f"{artifact.artifact_id}: missing dependency {dependency}")
        if not artifact.digest.startswith("sha256:"):
            errors.append(f"{artifact.artifact_id}: digest type is not declared")
    return errors


portfolio = (
    Artifact("contract", "problem_contract", "sha256:contract-example"),
    Artifact("baseline", "classical_baseline", "sha256:baseline-example", ("contract",)),
    Artifact("candidate", "labeled_experiment", "sha256:candidate-example", ("contract",)),
    Artifact("validator", "acceptance_test", "sha256:validator-example", ("contract",)),
    Artifact(
        "comparison",
        "evidence_comparison",
        "sha256:comparison-example",
        ("baseline", "candidate", "validator"),
    ),
    Artifact("decision", "decision_record", "sha256:decision-example", ("comparison",)),
)

assert validate_manifest(portfolio) == []
for item in portfolio:
    print(item.artifact_id, "<-", item.depends_on or ("root",))
