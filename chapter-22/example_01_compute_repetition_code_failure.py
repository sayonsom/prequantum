"""Compute the exact logical failure probability of a three-bit code."""

from __future__ import annotations

from itertools import product


def probability_of_pattern(pattern: tuple[int, ...], p: float) -> float:
    flips = sum(pattern)
    return (p**flips) * ((1.0 - p) ** (len(pattern) - flips))


def majority_decode(received: tuple[int, int, int]) -> int:
    return int(sum(received) >= 2)


def exact_logical_failure(p: float, logical_bit: int = 0) -> float:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be between zero and one")
    encoded = (logical_bit, logical_bit, logical_bit)
    failure = 0.0
    for error in product((0, 1), repeat=3):
        received = tuple(bit ^ flip for bit, flip in zip(encoded, error))
        if majority_decode(received) != logical_bit:
            failure += probability_of_pattern(error, p)
    return failure


for physical_error in (0.001, 0.01, 0.1, 0.5):
    enumerated = exact_logical_failure(physical_error)
    formula = 3 * physical_error**2 - 2 * physical_error**3
    assert abs(enumerated - formula) < 1e-15
    print(
        f"p={physical_error:.3f}  "
        f"unencoded={physical_error:.6f}  encoded={enumerated:.6f}"
    )
