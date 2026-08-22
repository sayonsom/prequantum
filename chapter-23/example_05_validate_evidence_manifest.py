"""Validate an experiment manifest against evidence-type requirements."""

from __future__ import annotations

from dataclasses import dataclass


EVIDENCE_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "mathematical_analysis": ("artifact_digest", "validator", "limitations"),
    "classical_exact": ("artifact_digest", "environment", "raw_output", "validator"),
    "classical_stochastic": (
        "artifact_digest",
        "environment",
        "sampling_policy",
        "raw_output",
        "validator",
    ),
    "quantum_simulator": (
        "artifact_digest",
        "environment",
        "sampling_policy",
        "raw_output",
        "validator",
    ),
    "quantum_hardware": (
        "artifact_digest",
        "hardware_identity",
        "compilation_record",
        "sampling_policy",
        "raw_output",
        "validator",
    ),
}


@dataclass(frozen=True)
class EvidenceManifest:
    evidence_type: str
    values: dict[str, str]


def missing_requirements(manifest: EvidenceManifest) -> list[str]:
    if manifest.evidence_type not in EVIDENCE_REQUIREMENTS:
        raise ValueError("unknown evidence type")
    required = EVIDENCE_REQUIREMENTS[manifest.evidence_type]
    return [name for name in required if not manifest.values.get(name, "").strip()]


manifest = EvidenceManifest(
    evidence_type="classical_stochastic",
    values={
        "artifact_digest": "sha256:example-only",
        "environment": "CPython standard library; environment manifest retained",
        "sampling_policy": "fixed pseudorandom seed and declared trial count",
        "raw_output": "local JSON record",
        "validator": "independent objective recomputation",
        "limitations": "pedagogical instance; not a scaling benchmark",
    },
)

assert missing_requirements(manifest) == []
hardware_version = EvidenceManifest("quantum_hardware", manifest.values)
assert missing_requirements(hardware_version) == [
    "hardware_identity",
    "compilation_record",
]
print("manifest accepted as:", manifest.evidence_type)
print("cannot be relabeled as hardware; missing:", missing_requirements(hardware_version))
