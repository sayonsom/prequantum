"""Compute stabilizer syndromes using Pauli-string commutation."""

from __future__ import annotations


def anticommutes(left: str, right: str) -> bool:
    if len(left) != len(right):
        raise ValueError("Pauli strings must have equal length")
    disagreements = sum(
        a != "I" and b != "I" and a != b for a, b in zip(left, right)
    )
    return bool(disagreements % 2)


def syndrome(error: str, generators: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(int(anticommutes(error, check)) for check in generators)


checks = ("ZZI", "IZZ")
errors = {
    "no error": "III",
    "X on q0": "XII",
    "X on q1": "IXI",
    "X on q2": "IIX",
}

expected = {
    "no error": (0, 0),
    "X on q0": (1, 0),
    "X on q1": (1, 1),
    "X on q2": (0, 1),
}

for label, error in errors.items():
    observed = syndrome(error, checks)
    assert observed == expected[label]
    print(f"{label:10s} {error} -> {observed}")
