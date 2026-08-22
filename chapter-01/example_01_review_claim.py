from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimRecord:
    task: str
    classical_baseline: str | None
    physical_hardware: bool
    end_to_end_metric: bool
    reproducible_method: bool
    future_target: bool = False


def classify(record: ClaimRecord) -> str:
    if record.future_target:
        return "roadmap statement"
    if record.physical_hardware and record.reproducible_method:
        if record.classical_baseline and record.end_to_end_metric:
            return "end-to-end comparison"
        return "device benchmark"
    if record.reproducible_method:
        return "simulation or analytical result"
    return "insufficiently specified claim"


benchmark = ClaimRecord(
    task="sample the output of a specified circuit family",
    classical_baseline="named classical simulation method",
    physical_hardware=True,
    end_to_end_metric=False,
    reproducible_method=True,
)
roadmap = ClaimRecord(
    task="run a future fault-tolerant workload",
    classical_baseline=None,
    physical_hardware=False,
    end_to_end_metric=False,
    reproducible_method=False,
    future_target=True,
)

print(classify(benchmark))
print(classify(roadmap))
# device benchmark
# roadmap statement
