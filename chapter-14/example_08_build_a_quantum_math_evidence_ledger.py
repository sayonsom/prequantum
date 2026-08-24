from dataclasses import dataclass


@dataclass(frozen=True)
class QuantumMathEvidence:
    object_definition: str
    basis_and_order: str
    units: str
    representation: str
    transformation: str
    approximation: str | None
    invariant_checks: tuple[str, ...]
    evidence_level: str
    supported_conclusion: str

    def validate(self):
        allowed_levels = {"analytic", "exact_numerical", "approximate_numerical", "hardware_observation"}
        if self.evidence_level not in allowed_levels:
            raise ValueError("unknown evidence level")
        if not self.object_definition or not self.basis_and_order or not self.representation:
            raise ValueError("object, basis, and representation records are required")
        if not self.invariant_checks:
            raise ValueError("at least one invariant check is required")
        if "product formula" in self.transformation.lower() and self.approximation is None:
            raise ValueError("a product-formula record requires an approximation statement")


record = QuantumMathEvidence(
    object_definition="H=-ZZ-0.5(XI+IX), total_time=1",
    basis_and_order="NumPy basis |00>, |01>, |10>, |11>",
    units="hbar=1",
    representation="4x4 complex Hermitian matrix",
    transformation="first-order A-then-B and symmetric second-order product formulas",
    approximation="operator 2-norm error against scipy.linalg.expm for steps 1 through 64",
    invariant_checks=("H=H_dagger", "U_dagger U=I", "error decreases on tested step grid"),
    evidence_level="approximate_numerical",
    supported_conclusion="the observed errors show first- and second-order slopes on this fixed instance",
)
record.validate()

quantumgridos_contracts = {
    "get_quantum_object_contract": "return object, dimensions, basis order, units, and assumptions",
    "get_quantum_transformation_ledger": "return exact or approximate map, parameters, and conventions",
    "get_quantum_invariant_report": "return checks, tolerances, references, failures, and bounded conclusion",
    "availability": "proposed companion interfaces; not executed by this example",
}

print(f"evidence_record={record}")
print(f"quantumgridos_contracts={quantumgridos_contracts}")
