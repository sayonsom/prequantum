"""Audit a multidimensional advantage claim without inventing a score."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AdvantageClaim:
    task_fidelity: str | None
    result_quality: str | None
    resources: str | None
    scale: str | None
    access: str | None
    reproducibility: str | None
    usefulness: str | None


def audit_claim(claim: AdvantageClaim) -> tuple[list[str], dict[str, str]]:
    missing: list[str] = []
    present: dict[str, str] = {}
    for field_name in claim.__dataclass_fields__:
        value = getattr(claim, field_name)
        if value is None or not value.strip():
            missing.append(field_name)
        else:
            present[field_name] = value
    return missing, present


claim = AdvantageClaim(
    task_fidelity="same declared graph family and objective",
    result_quality="independently recomputed objective with a stated tolerance",
    resources=None,
    scale="measured on a bounded instance family; no asymptotic conclusion",
    access="local simulator record only; no hardware access claimed",
    reproducibility="source, inputs, seed, and environment manifest retained",
    usefulness=None,
)

missing, present = audit_claim(claim)
assert missing == ["resources", "usefulness"]
assert set(present) == {
    "task_fidelity",
    "result_quality",
    "scale",
    "access",
    "reproducibility",
}
print("present:", ", ".join(present))
print("missing:", ", ".join(missing))
