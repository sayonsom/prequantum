"""Choose a finite Grover iteration count by testing adjacent integers."""

from math import asin, ceil, floor, pi, sin, sqrt


def success_probability(size, marked_count, iterations):
    theta = asin(sqrt(marked_count / size))
    return sin((2 * iterations + 1) * theta) ** 2


def best_first_peak_iteration(size, marked_count):
    theta = asin(sqrt(marked_count / size))
    continuous = pi / (4 * theta) - 0.5
    candidates = {0, max(0, floor(continuous)), max(0, ceil(continuous))}
    return max(
        candidates,
        key=lambda k: (success_probability(size, marked_count, k), -k),
    )


for size in (4, 8, 16, 32):
    iterations = best_first_peak_iteration(size, 1)
    probability = success_probability(size, 1, iterations)
    print(f"N={size:2d} k={iterations} exact_success={probability:.6f}")

print("N=8 trajectory:")
for iterations in range(6):
    probability = success_probability(8, 1, iterations)
    print(f"  k={iterations} success={probability:.6f}")

assert best_first_peak_iteration(8, 1) == 2
assert success_probability(8, 1, 2) > success_probability(8, 1, 1)
assert success_probability(8, 1, 3) < success_probability(8, 1, 2)
