"""Compute a deterministic paired bootstrap interval for synthetic observations."""

from __future__ import annotations

import random
from statistics import fmean


def paired_differences(
    candidate: list[float], baseline: list[float]
) -> list[float]:
    if len(candidate) != len(baseline) or not candidate:
        raise ValueError("paired samples must have equal nonzero length")
    return [left - right for left, right in zip(candidate, baseline)]


def bootstrap_mean_interval(
    differences: list[float], seed: int, resamples: int
) -> tuple[float, float, float]:
    generator = random.Random(seed)
    means: list[float] = []
    for _ in range(resamples):
        sample = [generator.choice(differences) for _ in differences]
        means.append(fmean(sample))
    means.sort()
    lower_index = int(0.025 * (resamples - 1))
    upper_index = int(0.975 * (resamples - 1))
    return fmean(differences), means[lower_index], means[upper_index]


baseline = [0.71, 0.76, 0.68, 0.81, 0.74, 0.79, 0.72, 0.77]
candidate = [0.73, 0.75, 0.72, 0.82, 0.78, 0.78, 0.76, 0.80]
differences = paired_differences(candidate, baseline)
mean, lower, upper = bootstrap_mean_interval(differences, seed=2304, resamples=5000)

assert round(mean, 6) == round(fmean(differences), 6)
assert lower <= mean <= upper
print("synthetic paired mean difference:", round(mean, 4))
print("synthetic bootstrap interval:", (round(lower, 4), round(upper, 4)))
