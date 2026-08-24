"""Enumerate asymmetric logical distances of the bit-flip repetition code."""

from __future__ import annotations

from itertools import product


def anticommutes(left: str, right: str) -> bool:
    disagreements = sum(
        a != "I" and b != "I" and a != b for a, b in zip(left, right)
    )
    return bool(disagreements % 2)


def weight(pauli: str) -> int:
    return sum(symbol != "I" for symbol in pauli)


checks = ("ZZI", "IZZ")
stabilizers = {"III", "ZZI", "IZZ", "ZIZ"}
normalizer = {
    "".join(candidate)
    for candidate in product("IXYZ", repeat=3)
    if all(not anticommutes("".join(candidate), check) for check in checks)
}
logical = normalizer - stabilizers

x_only = [item for item in logical if set(item) <= {"I", "X"}]
z_only = [item for item in logical if set(item) <= {"I", "Z"}]

x_distance = min(map(weight, x_only))
z_distance = min(map(weight, z_only))
full_distance = min(map(weight, logical))

assert (x_distance, z_distance, full_distance) == (3, 1, 1)
print("X distance:", x_distance)
print("Z distance:", z_distance)
print("full quantum distance:", full_distance)
