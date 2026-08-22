"""Build and identify a solver-independent problem contract."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProblemContract:
    name: str
    input_family: str
    required_output: str
    correctness_test: str
    approximation_rule: str
    counted_resources: tuple[str, ...]
    intended_user: str


def canonical_bytes(contract: ProblemContract) -> bytes:
    payload = json.dumps(
        asdict(contract), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return payload.encode("utf-8")


contract = ProblemContract(
    name="small weighted cut study",
    input_family="undirected weighted graphs from a declared generator",
    required_output="a binary partition and its independently recomputed cut value",
    correctness_test="every vertex appears once and the reported value is reproducible",
    approximation_rule="report the gap to an exact optimum when enumeration is feasible",
    counted_resources=(
        "preprocessing",
        "solver execution",
        "sampling",
        "postprocessing",
        "validation",
    ),
    intended_user="a developer learning fair benchmark design",
)

encoded = canonical_bytes(contract)
digest = hashlib.sha256(encoded).hexdigest()
recovered = json.loads(encoded)

assert recovered["name"] == contract.name
assert len(digest) == 64
print(encoded.decode("utf-8"))
print("contract_sha256:", digest)
