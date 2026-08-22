"""Compare exact and bounded-error query contracts without mixing cost models."""

from math import comb


def dj_balanced_misclassification_probability(width, distinct_queries):
    size = 2**width
    half = size // 2
    if distinct_queries > half:
        return 0.0
    return 2 * comb(half, distinct_queries) / comb(size, distinct_queries)


width = 8
exact_classical_dj = 2 ** (width - 1) + 1
exact_quantum_dj = 1

print("Deutsch-Jozsa exact deterministic queries:")
print("  classical:", exact_classical_dj)
print("  quantum:  ", exact_quantum_dj)

for queries in (1, 2, 3, 4):
    failure = dj_balanced_misclassification_probability(width, queries)
    print(f"randomized classical queries={queries} conditional failure={failure:.4f}")

assert dj_balanced_misclassification_probability(width, 3) < 1 / 3

exact_classical_bv = width
exact_quantum_bv = 1
print("Bernstein-Vazirani exact queries:")
print("  classical:", exact_classical_bv)
print("  quantum:  ", exact_quantum_bv)

assert exact_classical_dj > exact_classical_bv > 1
assert exact_quantum_dj == exact_quantum_bv == 1

# These counts ignore oracle construction, non-query gates, shots, and runtime.
