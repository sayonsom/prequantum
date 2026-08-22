from dataclasses import dataclass


EVIDENCE_LEVELS = {
    "exact_derivation",
    "ideal_statevector",
    "ideal_sampled",
    "declared_noise_model",
    "hardware_observation",
}


@dataclass(frozen=True)
class OrderFindingLedger:
    modulus: int
    base: int
    counting_qubits: int
    controlled_power_calls: int
    multiplier_implementation: str
    evidence_level: str
    shots: int
    compiled_two_qubit_gates: int | None = None
    logical_qubits: int | None = None
    logical_cycles: int | None = None
    code_family: str | None = None
    physical_error_model: str | None = None
    cycle_time: str | None = None

    def validate(self):
        if self.evidence_level not in EVIDENCE_LEVELS:
            raise ValueError("unknown evidence level")
        if self.controlled_power_calls != self.counting_qubits:
            raise ValueError("record one controlled power per counting qubit")
        sampled_levels = {"ideal_sampled", "declared_noise_model", "hardware_observation"}
        if self.evidence_level in sampled_levels and self.shots <= 0:
            raise ValueError("sampled evidence requires a positive shot count")
        if self.evidence_level == "ideal_statevector" and self.shots != 0:
            raise ValueError("an exact statevector calculation does not use shots")

    def missing_for_physical_feasibility(self):
        required = {
            "compiled_two_qubit_gates": self.compiled_two_qubit_gates,
            "logical_qubits": self.logical_qubits,
            "logical_cycles": self.logical_cycles,
            "code_family": self.code_family,
            "physical_error_model": self.physical_error_model,
            "cycle_time": self.cycle_time,
        }
        return [name for name, value in required.items() if value is None]


ledger = OrderFindingLedger(
    modulus=15,
    base=2,
    counting_qubits=4,
    controlled_power_calls=4,
    multiplier_implementation="dense educational permutation matrix",
    evidence_level="ideal_statevector",
    shots=0,
)
ledger.validate()
missing = ledger.missing_for_physical_feasibility()

assert missing == [
    "compiled_two_qubit_gates",
    "logical_qubits",
    "logical_cycles",
    "code_family",
    "physical_error_model",
    "cycle_time",
]

print(f"evidence_level={ledger.evidence_level}")
print(f"high_level_controlled_power_calls={ledger.controlled_power_calls}")
print(f"multiplier_implementation={ledger.multiplier_implementation}")
print(f"missing_for_physical_feasibility={missing}")
print("supported_claim=the declared ideal small-instance calculation recovers order four")
