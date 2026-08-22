"""Separate an active Hadamard gate from a passive coordinate conversion."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
one = np.array([0.0, 1.0], dtype=complex)
h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

# The columns of B are the |+> and |-> basis vectors in standard coordinates.
basis_x = h
psi_standard = np.array([np.sqrt(3) / 2, 0.5j], dtype=complex)

# Passive change: the abstract state stays fixed; only its coordinate list changes.
coordinates_x = basis_x.conj().T @ psi_standard
reconstructed = basis_x @ coordinates_x

# Active operation: H acts on the state while standard coordinates stay fixed.
after_active_h = h @ psi_standard

print("state in standard coordinates:", np.round(psi_standard, 4))
print("same state in X coordinates:    ", np.round(coordinates_x, 4))
print("new state after active H:       ", np.round(after_active_h, 4))

assert np.allclose(reconstructed, psi_standard)
assert np.allclose(coordinates_x, after_active_h)
assert not np.allclose(reconstructed, after_active_h)

# The two arrays match here because H is unitary, Hermitian, and its own inverse.
# Their meanings differ: one labels the old state in a new basis; one is a new state.
