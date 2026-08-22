"""Verify a phase oracle built from the projector onto a marked subspace."""

import numpy as np


size = 8
marked = {2, 5}
projector_good = np.zeros((size, size), dtype=complex)
for index in marked:
    projector_good[index, index] = 1.0

oracle = np.eye(size, dtype=complex) - 2 * projector_good

for index in range(size):
    basis = np.eye(size, dtype=complex)[:, index]
    expected_sign = -1 if index in marked else 1
    actual = oracle @ basis
    assert np.allclose(actual, expected_sign * basis)
    print(f"x={index:03b} marked={index in marked} sign={expected_sign:+d}")

assert np.allclose(projector_good @ projector_good, projector_good)
assert np.allclose(oracle.conj().T, oracle)
assert np.allclose(oracle.conj().T @ oracle, np.eye(size))
assert np.allclose(oracle @ oracle, np.eye(size))
