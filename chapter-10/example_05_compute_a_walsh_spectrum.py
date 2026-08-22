"""Compute the interference spectrum produced by one phase query."""

import numpy as np


values = np.array([0, 0, 0, 1, 1, 1, 1, 0], dtype=int)
width = 3
size = 2**width


def binary_inner_product(left, right):
    return (left & right).bit_count() % 2


amplitudes = np.zeros(size, dtype=complex)
for output_label in range(size):
    amplitudes[output_label] = sum(
        (-1) ** (values[x] + binary_inner_product(x, output_label))
        for x in range(size)
    ) / size

probabilities = np.abs(amplitudes) ** 2
for label, (amplitude, probability) in enumerate(zip(amplitudes, probabilities)):
    print(f"z={label:03b} amplitude={amplitude.real:+.3f} p={probability:.3f}")

assert values.sum() == size // 2
assert np.isclose(amplitudes[0], 0.0)
assert np.isclose(probabilities.sum(), 1.0)
assert np.count_nonzero(probabilities > 1e-12) > 1

# Deutsch-Jozsa needs only the zero-label amplitude. The other amplitudes retain
# information about the function's Walsh spectrum, but one sample cannot reveal it all.
