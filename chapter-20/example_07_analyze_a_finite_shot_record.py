"""Attach uncertainty and a bounded comparison to a finite-shot record."""

from __future__ import annotations

from math import sqrt


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    proportion = successes / trials
    denominator = 1 + z**2 / trials
    center = (proportion + z**2 / (2 * trials)) / denominator
    radius = (
        z
        * sqrt(proportion * (1 - proportion) / trials + z**2 / (4 * trials**2))
        / denominator
    )
    return center - radius, center + radius


counts = {"00": 1960, "01": 120, "10": 140, "11": 1876}
shots = sum(counts.values())
probabilities = {state: count / shots for state, count in counts.items()}
ideal = {"00": 0.5, "01": 0.0, "10": 0.0, "11": 0.5}

correlated = counts["00"] + counts["11"]
correlation_rate = correlated / shots
interval = wilson_interval(correlated, shots)
total_variation = 0.5 * sum(
    abs(probabilities[state] - ideal[state]) for state in ideal
)

print(f"shots={shots}")
print(f"correlated outcomes={correlation_rate:.4f}")
print(f"95% Wilson interval=({interval[0]:.4f}, {interval[1]:.4f})")
print(f"total-variation distance from ideal Bell distribution={total_variation:.4f}")

assert 0 <= total_variation <= 1
assert interval[0] <= correlation_rate <= interval[1]

