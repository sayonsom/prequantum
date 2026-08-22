from dataclasses import dataclass


EVIDENCE_ORDER = {
    "analytic": 0,
    "ideal_statevector": 1,
    "finite_shot_simulation": 2,
    "noise_model_simulation": 3,
    "hardware_observation": 4,
}


@dataclass(frozen=True)
class VariationalEvidence:
    problem: str
    operator_and_offset: str
    state_family: str
    estimator: str
    optimizer_and_seed: str
    classical_reference: str | None
    quantum_resources: str
    end_to_end_resource_accounting: bool
    evidence_level: str

    def validate(self):
        if self.evidence_level not in EVIDENCE_ORDER:
            raise ValueError("unknown evidence level")
        if not self.operator_and_offset:
            raise ValueError("operator and constant-offset convention are required")
        if not self.estimator or not self.quantum_resources:
            raise ValueError("estimator and resource fields are required")


def audit_claim(record, requested_claim):
    record.validate()
    if requested_claim == "scalable_quantum_advantage":
        missing = []
        if record.evidence_level != "hardware_observation":
            missing.append("hardware observation")
        if record.classical_reference is None:
            missing.append("credible classical reference")
        if not record.end_to_end_resource_accounting:
            missing.append("end-to-end resource accounting")
        return {"accepted": not missing, "missing": missing}
    return {"accepted": True, "missing": []}


record = VariationalEvidence(
    problem="four-node cycle MaxCut",
    operator_and_offset="C=sum(1-ZuZv)/2; offset=2",
    state_family="ideal p=1 QAOA",
    estimator="exact statevector expectation plus seeded samples",
    optimizer_and_seed="bounded L-BFGS-B after a fixed grid; seed=211 for samples",
    classical_reference="exhaustive evaluation of all sixteen assignments",
    quantum_resources="four ideal qubits; no compilation or noise model",
    end_to_end_resource_accounting=False,
    evidence_level="ideal_statevector",
)

audit = audit_claim(record, "scalable_quantum_advantage")
quantumgridos_contract = {
    "proposed_tool": "get_variational_run_evidence",
    "input": "problem, operator, state family, estimator, optimizer, resources",
    "output": "validated evidence ledger and strongest supported conclusion",
    "availability": "proposed companion interface; not executed by this example",
}

assert audit["accepted"] is False
assert audit["missing"] == ["hardware observation", "end-to-end resource accounting"]

print(f"record={record}")
print(f"advantage_claim_audit={audit}")
print(f"quantumgridos_contract={quantumgridos_contract}")
