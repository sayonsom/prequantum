"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.3 Density Matrices: Beyond Pure States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_08_density_matrices_beyond_pure_states.py
"""

import numpy as np

# Pure state: |+⟩ = (|0⟩ + |1⟩)/√2
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho_pure = np.outer(plus, plus.conj())  # ρ = |ψ⟩⟨ψ|

print("Pure state |+⟩ density matrix:")
print(np.round(rho_pure, 4))
print(f"Tr(ρ) = {np.trace(rho_pure).real:.4f}")
print(f"Tr(ρ²) = {np.trace(rho_pure @ rho_pure).real:.4f}")  # 1.0 for pure states
print()

# Mixed state: 70% |0⟩, 30% |1⟩ (classical uncertainty, not superposition)
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
rho_mixed = 0.7 * np.outer(ket_0, ket_0.conj()) + 0.3 * np.outer(ket_1, ket_1.conj())

print("Mixed state (70% |0⟩, 30% |1⟩) density matrix:")
print(np.round(rho_mixed, 4))
print(f"Tr(ρ) = {np.trace(rho_mixed).real:.4f}")
print(f"Tr(ρ²) = {np.trace(rho_mixed @ rho_mixed).real:.4f}")  # < 1 for mixed states
# Output:
# Pure state |+⟩ density matrix:
# [[0.5+0.j 0.5+0.j]
#  [0.5+0.j 0.5+0.j]]
# Tr(ρ) = 1.0000
# Tr(ρ²) = 1.0000
#
# Mixed state (70% |0⟩, 30% |1⟩) density matrix:
# [[0.7+0.j 0. +0.j]
#  [0. +0.j 0.3+0.j]]
# Tr(ρ) = 1.0000
# Tr(ρ²) = 0.5800
