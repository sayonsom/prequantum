from dataclasses import dataclass
from typing import Literal


TargetKind = Literal["analytical", "simulator", "qpu"]


@dataclass(frozen=True)
class ExecutionRecord:
    program_name: str
    target_kind: TargetKind
    target_name: str
    samples: int
    result_kind: str

    def validate(self) -> None:
        if self.samples < 1:
            raise ValueError("samples must be positive")
        if self.target_kind == "qpu" and self.result_kind == "state_vector":
            raise ValueError(
                "a hardware run should not claim direct access to a full state vector"
            )


run = ExecutionRecord(
    program_name="one-qubit measurement",
    target_kind="simulator",
    target_name="local teaching simulator",
    samples=1000,
    result_kind="measurement_counts",
)
run.validate()
print(run.target_kind, run.result_kind)
# simulator measurement_counts
