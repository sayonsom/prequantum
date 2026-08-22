"""Trace how a value oracle writes a function value into relative phase."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
one = np.array([0.0, 1.0], dtype=complex)
plus = (zero + one) / np.sqrt(2)
minus = (zero - one) / np.sqrt(2)

# Tensor order is input, output. This CNOT implements f(x)=x.
oracle = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=complex,
)

for label, x, phase in (("0", zero, 1), ("1", one, -1)):
    actual = oracle @ np.kron(x, minus)
    expected = phase * np.kron(x, minus)
    print(f"x={label} phase={phase:+d} match={np.allclose(actual, expected)}")
    assert np.allclose(actual, expected)

actual_superposition = oracle @ np.kron(plus, minus)
expected_superposition = np.kron(minus, minus)
assert np.allclose(actual_superposition, expected_superposition)

# The output remains |->, while the input changes from |+> to |->.
amplitude_table = actual_superposition.reshape(2, 2)
assert np.allclose(amplitude_table[0], minus / np.sqrt(2))
assert np.allclose(amplitude_table[1], -minus / np.sqrt(2))
