"""Group single-qubit Shor-code errors by their stabilizer syndrome."""

from __future__ import annotations

from collections import defaultdict


def anticommutes(left: str, right: str) -> bool:
    disagreements = sum(
        a != "I" and b != "I" and a != b for a, b in zip(left, right)
    )
    return bool(disagreements % 2)


def syndrome(error: str, checks: tuple[str, ...]) -> str:
    return "".join("1" if anticommutes(error, check) else "0" for check in checks)


generators = (
    "ZZIIIIIII",
    "IZZIIIIII",
    "IIIZZIIII",
    "IIIIZZIII",
    "IIIIIIZZI",
    "IIIIIIIZZ",
    "XXXXXXIII",
    "IIIXXXXXX",
)

groups: dict[str, list[str]] = defaultdict(list)
for qubit in range(9):
    for symbol in "XYZ":
        error = "I" * qubit + symbol + "I" * (8 - qubit)
        groups[syndrome(error, generators)].append(f"{symbol}{qubit}")

assert sum(map(len, groups.values())) == 27
for observed, labels in sorted(groups.items()):
    print(observed, ", ".join(labels))
