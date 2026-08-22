"""Distinguish the ambient vector space from normalized physical statevectors."""

import numpy as np


psi = np.array([1.0, 0.0], dtype=complex)
phi = np.array([0.0, 1.0], dtype=complex)

sum_vector = psi + phi
scaled_vector = 2.0 * psi

def norm(vector):
    return float(np.linalg.norm(vector))


print("norm(|0>):       ", norm(psi))
print("norm(|1>):       ", norm(phi))
print("norm(|0> + |1>): ", norm(sum_vector))
print("norm(2|0>):      ", norm(scaled_vector))

assert np.isclose(norm(psi), 1.0)
assert np.isclose(norm(phi), 1.0)
assert not np.isclose(norm(sum_vector), 1.0)
assert not np.isclose(norm(scaled_vector), 1.0)

# C^2 is closed under addition and scalar multiplication. Its unit sphere is not.
normalized_sum = sum_vector / norm(sum_vector)
assert np.isclose(norm(normalized_sum), 1.0)
