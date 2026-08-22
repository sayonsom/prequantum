"""Simulate a randomized Grover schedule when the marked count is unknown."""

from math import asin, ceil, sin, sqrt

import numpy as np


def one_unknown_count_search(size, marked_count, rng, growth=6 / 5):
    """Return ideal query cost for one successful randomized search."""
    theta = asin(sqrt(marked_count / size))
    window = 1.0
    queries = 0

    while True:
        iterations = int(rng.integers(0, max(1, ceil(window))))
        queries += iterations
        success = sin((2 * iterations + 1) * theta) ** 2

        # Verification is one additional predicate query.
        queries += 1
        if rng.random() < success:
            return queries

        window = min(growth * window, sqrt(size))


size = 256
trials = 5000
for marked_count in (1, 5, 32):
    rng = np.random.default_rng(73 + marked_count)
    costs = np.array(
        [one_unknown_count_search(size, marked_count, rng) for _ in range(trials)]
    )
    scale = sqrt(size / marked_count)
    print(
        f"M={marked_count:2d} mean_queries={costs.mean():.3f} "
        f"sqrt(N/M)={scale:.3f}"
    )
    assert costs.mean() < 4 * scale + 2

# The experiment models ideal good/bad-subspace probabilities and query counts.
# It does not model a gate decomposition, noise, or wall-clock runtime.
