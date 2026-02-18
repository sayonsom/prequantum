"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.3 Basis: What Makes a Set of Vectors a Basis
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_04_basis_what_makes_a_set_of_vectors_a_basi.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

# Computational basis: {|0⟩, |1⟩}
# Hadamard basis:      {|+⟩, |−⟩}

# Both are valid bases because:
# 1. They're orthogonal (inner product = 0)
print(f"⟨0|1⟩ = {np.dot(ket_0.conj(), ket_1):.4f}")        # 0
print(f"⟨+|−⟩ = {np.dot(ket_plus.conj(), ket_minus):.4f}")  # 0

# 2. They're normalized (inner product with self = 1)
print(f"⟨0|0⟩ = {np.dot(ket_0.conj(), ket_0):.4f}")        # 1
print(f"⟨+|+⟩ = {np.dot(ket_plus.conj(), ket_plus):.4f}")  # 1

# 3. They span the space (any state can be written as a combo)
psi = np.array([0.6+0j, 0.8+0j])

# Express |ψ⟩ in computational basis
alpha_0 = np.dot(ket_0.conj(), psi)
alpha_1 = np.dot(ket_1.conj(), psi)
print(f"\n|ψ⟩ in comp. basis: {alpha_0:.4f}|0⟩ + {alpha_1:.4f}|1⟩")

# Express |ψ⟩ in Hadamard basis
beta_plus = np.dot(ket_plus.conj(), psi)
beta_minus = np.dot(ket_minus.conj(), psi)
print(f"|ψ⟩ in Had. basis:  {beta_plus:.4f}|+⟩ + {beta_minus:.4f}|−⟩")

# Verify reconstruction
reconstructed_comp = alpha_0 * ket_0 + alpha_1 * ket_1
reconstructed_had = beta_plus * ket_plus + beta_minus * ket_minus
print(f"\nReconstruct from comp: {np.round(reconstructed_comp, 4)}")
print(f"Reconstruct from had:  {np.round(reconstructed_had, 4)}")
print(f"Same? {np.allclose(reconstructed_comp, reconstructed_had)}")  # True
