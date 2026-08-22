"""Build basis projectors with outer products and test completeness."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
one = np.array([0.0, 1.0], dtype=complex)
p_zero = np.outer(zero, zero.conj())
p_one = np.outer(one, one.conj())

psi = np.array([np.sqrt(0.65), np.exp(0.8j) * np.sqrt(0.35)], dtype=complex)
probability_zero = float(np.vdot(psi, p_zero @ psi).real)
probability_one = float(np.vdot(psi, p_one @ psi).real)

print("P0 =\n", p_zero)
print("P1 =\n", p_one)
print("probabilities:", probability_zero, probability_one)

assert np.allclose(p_zero @ p_zero, p_zero)
assert np.allclose(p_one @ p_one, p_one)
assert np.allclose(p_zero.conj().T, p_zero)
assert np.allclose(p_one.conj().T, p_one)
assert np.allclose(p_zero + p_one, np.eye(2))
assert np.isclose(probability_zero + probability_one, 1.0)
