"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.5 Density Matrices: A Preview
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_08_density_matrices_a_preview.py
"""

import numpy as np

# Pure state |+⟩ = (|0⟩ + |1⟩)/√2
plus = np.array([1, 1]) / np.sqrt(2)
rho_pure = np.outer(plus, plus.conj())
print("Pure |+⟩ density matrix:")
print(np.round(rho_pure, 3))
print(f"  Purity Tr(ρ²) = {np.trace(rho_pure @ rho_pure):.3f}")  # = 1.0

# Mixed state: 50% |0⟩ + 50% |1⟩ (classical mixture, NOT superposition!)
zero = np.array([1, 0])
one = np.array([0, 1])
rho_mixed = 0.5 * np.outer(zero, zero) + 0.5 * np.outer(one, one)
print("\nClassical mixture (50% |0⟩ + 50% |1⟩) density matrix:")
print(np.round(rho_mixed, 3))
print(f"  Purity Tr(ρ²) = {np.trace(rho_mixed @ rho_mixed):.3f}")  # = 0.5

# Maximally mixed state (center of Bloch sphere -- no quantum info left)
rho_max_mixed = np.eye(2) / 2
print("\nMaximally mixed state (I/2) density matrix:")
print(np.round(rho_max_mixed, 3))
print(f"  Purity Tr(ρ²) = {np.trace(rho_max_mixed @ rho_max_mixed):.3f}")  # = 0.5

# Key insight: |+⟩ and the classical 50/50 mixture give the SAME measurement
# statistics in the Z basis (both are 50/50), but they're different states.
# The off-diagonal elements encode the phase -- and noise destroys them.
print("\nKey difference: off-diagonal elements (coherences)")
print(f"  Pure |+⟩:    ρ[0,1] = {rho_pure[0,1]:.3f}")
print(f"  Mixed 50/50: ρ[0,1] = {rho_mixed[0,1]:.3f}")
print("  Dephasing (T2 decay) kills these off-diagonals.")
