"""Extract and reconstruct coordinates in a complex orthonormal basis."""

import numpy as np


plus_i = np.array([1.0, 1.0j], dtype=complex) / np.sqrt(2)
minus_i = np.array([1.0, -1.0j], dtype=complex) / np.sqrt(2)
basis_y = np.column_stack([plus_i, minus_i])

psi = np.array([np.sqrt(0.7), np.exp(0.4j) * np.sqrt(0.3)], dtype=complex)
coordinates = basis_y.conj().T @ psi
reconstructed = basis_y @ coordinates

print("B^dagger B =\n", np.round(basis_y.conj().T @ basis_y, 5))
print("Y-basis coordinates:", np.round(coordinates, 5))

assert np.allclose(basis_y.conj().T @ basis_y, np.eye(2))
assert np.allclose(reconstructed, psi)
assert np.isclose(np.vdot(coordinates, coordinates).real, 1.0)

# Replacing conjugate transpose with ordinary transpose breaks reconstruction.
wrong_coordinates = basis_y.T @ psi
assert not np.allclose(basis_y @ wrong_coordinates, psi)
