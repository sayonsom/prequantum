"""Explore a declared toy model of below- and above-threshold scaling."""

from __future__ import annotations


def toy_logical_error(
    physical_error: float,
    distance: int,
    *,
    threshold: float = 0.01,
    prefactor: float = 0.1,
) -> float:
    if distance < 1 or distance % 2 == 0:
        raise ValueError("distance must be a positive odd integer")
    if physical_error < 0 or threshold <= 0 or prefactor <= 0:
        raise ValueError("rates and prefactor must be valid")
    exponent = (distance + 1) // 2
    return prefactor * (physical_error / threshold) ** exponent


for physical_error in (0.003, 0.015):
    values = [toy_logical_error(physical_error, distance) for distance in (3, 5, 7)]
    direction = "decreases" if values[-1] < values[0] else "increases"
    print(f"assumed p={physical_error:.3f}: {values} -> {direction} with distance")

assert toy_logical_error(0.003, 7) < toy_logical_error(0.003, 3)
assert toy_logical_error(0.015, 7) > toy_logical_error(0.015, 3)
