"""Inspect a fixed two-qubit H2 Hamiltonian used in Qiskit tutorials."""

import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Coefficients from the H2 operator used in official Qiskit Algorithms tutorials.
terms = {
    "II": (-1.052373245772859, np.kron(I, I)),
    "IZ": (0.39793742484318045, np.kron(I, Z)),
    "ZI": (-0.39793742484318045, np.kron(Z, I)),
    "ZZ": (-0.01128010425623538, np.kron(Z, Z)),
    "XX": (0.18093119978423156, np.kron(X, X)),
}
H = sum(coefficient * pauli for coefficient, pauli in terms.values())

eigenvalues, eigenvectors = np.linalg.eigh(H)
ground_state = eigenvectors[:, 0]
ground_energy = eigenvalues[0]
print(f"reference electronic ground energy: {ground_energy:.6f} Ha")

print("ground-state energy contributions")
contribution_sum = 0.0
for label, (coefficient, pauli) in terms.items():
    contribution = coefficient * np.vdot(ground_state, pauli @ ground_state).real
    contribution_sum += contribution
    print(f"  {label}: {contribution: .6f} Ha")
assert np.isclose(contribution_sum, ground_energy, atol=1e-12)

# Dynamics is a different task from finding the ground state.
psi_0 = np.array([0, 1, 0, 0], dtype=complex)
psi_t = expm(-1j * H * 1.0) @ psi_0
print("P(t=1):", np.round(np.abs(psi_t) ** 2, 6))

