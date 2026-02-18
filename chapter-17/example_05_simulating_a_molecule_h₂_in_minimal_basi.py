"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.4 Simulating a Molecule: H₂ in Minimal Basis
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_05_simulating_a_molecule_h₂_in_minimal_basi.py
"""

import numpy as np
from scipy.linalg import expm

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def h2_hamiltonian(bond_length):
    """Build the 2-qubit Hamiltonian for H₂ at a given bond length.
    Coefficients from Bravyi-Kitaev transformation of STO-3G integrals.
    Approximate values for illustration."""
    # These coefficients vary with bond length
    # (In practice, you'd compute them with PySCF or OpenFermion)
    if bond_length < 0.5:
        g0, g1, g2, g3, g4 = -0.40, 0.18, 0.18, -0.01, 0.18
    elif bond_length < 1.0:
        g0, g1, g2, g3, g4 = -1.05, 0.40, 0.40, -0.11, 0.18
    elif bond_length < 1.5:
        g0, g1, g2, g3, g4 = -1.14, 0.34, 0.34, -0.09, 0.17
    else:
        g0, g1, g2, g3, g4 = -1.06, 0.28, 0.28, -0.07, 0.16

    H = (g0 * np.kron(I, I) +
         g1 * np.kron(I, Z) +
         g2 * np.kron(Z, I) +
         g3 * np.kron(Z, Z) +
         g4 * np.kron(X, X))
    return H

# Compute ground state energy vs bond length (potential energy surface)
bond_lengths = np.linspace(0.3, 2.5, 12)
energies = []

print(f"{'Bond (Å)':>10}  {'E_ground (Ha)':>14}  {'E_excited (Ha)':>14}  {'Gap (Ha)':>10}")
print("-" * 52)
for r in bond_lengths:
    H = h2_hamiltonian(r)
    evals = np.linalg.eigvalsh(H)
    energies.append(evals[0])
    print(f"{r:>10.2f}  {evals[0]:>14.6f}  {evals[1]:>14.6f}  {evals[1]-evals[0]:>10.6f}")

# Find equilibrium bond length
min_idx = np.argmin(energies)
print(f"\nEquilibrium bond length: ~{bond_lengths[min_idx]:.2f} Å")
print(f"Ground state energy: {energies[min_idx]:.6f} Ha")
# Output:
# Bond (Å)   E_ground (Ha)  E_excited (Ha)    Gap (Ha)
# ----------------------------------------------------
#       0.30       -0.8125       -0.5700       0.2425
#       0.50       -1.9800       -1.1200       0.8600
#       0.70       -1.9800       -1.1200       0.8600
#       0.90       -1.9800       -1.1200       0.8600
#       1.10       -1.9309       -1.2200       0.7109
#       1.30       -1.9309       -1.2200       0.7109
#       1.50       -1.7124       -1.1500       0.5624
#       ...        (dissociation region)
#
# Equilibrium bond length: ~0.50 Å
# Ground state energy: -1.980000 Ha
