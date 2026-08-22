"""Distinguish a three-qubit encoding from three cloned copies."""

from __future__ import annotations

from math import sqrt


def tensor(left: dict[str, complex], right: dict[str, complex]) -> dict[str, complex]:
    return {
        left_bits + right_bits: left_amp * right_amp
        for left_bits, left_amp in left.items()
        for right_bits, right_amp in right.items()
        if abs(left_amp * right_amp) > 1e-12
    }


alpha = sqrt(3) / 2
beta = 0.5j
psi = {"0": alpha, "1": beta}

encoded = {"000": alpha, "111": beta}
three_copies = tensor(tensor(psi, psi), psi)

assert abs(sum(abs(a) ** 2 for a in encoded.values()) - 1.0) < 1e-12
assert abs(sum(abs(a) ** 2 for a in three_copies.values()) - 1.0) < 1e-12
assert encoded != three_copies

print("encoded support:", sorted(encoded))
print("three-copy support:", sorted(three_copies))
print("same state:", encoded == three_copies)
