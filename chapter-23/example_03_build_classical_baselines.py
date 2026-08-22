"""Build exact, greedy, and seeded-random baselines for weighted MaxCut."""

from __future__ import annotations

import random
from itertools import product


Edge = tuple[int, int, int]
EDGES: tuple[Edge, ...] = (
    (0, 1, 4),
    (0, 2, 2),
    (1, 2, 3),
    (1, 3, 5),
    (2, 4, 6),
    (3, 4, 1),
)
VERTICES = 5


def cut_value(bits: tuple[int, ...]) -> int:
    if len(bits) != VERTICES or set(bits) - {0, 1}:
        raise ValueError("bits must assign every vertex to zero or one")
    return sum(weight for left, right, weight in EDGES if bits[left] != bits[right])


def exact_baseline() -> tuple[tuple[int, ...], int]:
    candidates = product((0, 1), repeat=VERTICES)
    return max(((bits, cut_value(bits)) for bits in candidates), key=lambda item: item[1])


def greedy_baseline() -> tuple[tuple[int, ...], int]:
    bits = [0] * VERTICES
    for vertex in range(VERTICES):
        zero = tuple(bits)
        bits[vertex] = 1
        one = tuple(bits)
        bits[vertex] = int(cut_value(one) > cut_value(zero))
    result = tuple(bits)
    return result, cut_value(result)


def random_baseline(seed: int, trials: int) -> tuple[tuple[int, ...], int]:
    generator = random.Random(seed)
    candidates = [
        tuple(generator.randrange(2) for _ in range(VERTICES)) for _ in range(trials)
    ]
    return max(((bits, cut_value(bits)) for bits in candidates), key=lambda item: item[1])


exact_bits, exact_value = exact_baseline()
greedy_bits, greedy_value = greedy_baseline()
random_bits, random_value = random_baseline(seed=23, trials=32)

assert cut_value(exact_bits) == exact_value
assert greedy_value <= exact_value
assert random_value <= exact_value
print("exact:", exact_bits, exact_value)
print("greedy:", greedy_bits, greedy_value)
print("seeded random:", random_bits, random_value)
