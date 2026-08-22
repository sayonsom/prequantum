"""Test that the Grover diffuser reflects complex amplitudes about their mean."""

import numpy as np


amplitudes = np.array(
    [0.30 + 0.10j, -0.20 + 0.25j, 0.05 - 0.30j, 0.40 + 0.00j],
    dtype=complex,
)
size = len(amplitudes)
uniform = np.ones(size, dtype=complex) / np.sqrt(size)
diffuser = 2 * np.outer(uniform, uniform.conj()) - np.eye(size)

mean = amplitudes.mean()
expected = 2 * mean - amplitudes
actual = diffuser @ amplitudes

for index, (before, after) in enumerate(zip(amplitudes, actual)):
    print(f"x={index:02b} before={before:+.3f} after={after:+.3f}")

assert np.allclose(actual, expected)
assert np.allclose(diffuser @ uniform, uniform)

orthogonal = np.array([1, -1, 0, 0], dtype=complex) / np.sqrt(2)
assert np.allclose(np.vdot(uniform, orthogonal), 0.0)
assert np.allclose(diffuser @ orthogonal, -orthogonal)
assert np.allclose(diffuser.conj().T @ diffuser, np.eye(size))
