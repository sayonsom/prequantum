"""Evolve a two-qubit transverse-field Ising model exactly."""

import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# System and generator records. The basis order is |00>, |01>, |10>, |11>.
J = 1.0
h = 0.7
H = J * np.kron(Z, Z) + h * (np.kron(X, I) + np.kron(I, X))
psi_0 = np.array([1, 0, 0, 0], dtype=complex)

magnetization = 0.5 * (np.kron(Z, I) + np.kron(I, Z))
energy_0 = np.vdot(psi_0, H @ psi_0).real

print(" t    P(00)   P(01)   P(10)   P(11)    <M_z>    <H>")
for t in np.linspace(0.0, 1.5, 7):
    psi_t = expm(-1j * H * t) @ psi_0
    probabilities = np.abs(psi_t) ** 2
    mean_mz = np.vdot(psi_t, magnetization @ psi_t).real
    mean_energy = np.vdot(psi_t, H @ psi_t).real
    assert np.isclose(probabilities.sum(), 1.0, atol=1e-12)
    assert np.isclose(mean_energy, energy_0, atol=1e-12)
    print(
        f"{t:3.2f}  "
        + "  ".join(f"{p:6.3f}" for p in probabilities)
        + f"   {mean_mz:7.3f}  {mean_energy:6.3f}"
    )

