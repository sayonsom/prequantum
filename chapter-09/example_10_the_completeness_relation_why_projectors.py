"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.7 The Completeness Relation: Why Projectors Sum to Identity
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_10_the_completeness_relation_why_projectors.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

# Completeness relation: sum of projectors = identity
# Computational basis:
I_comp = np.outer(ket_0, ket_0.conj()) + np.outer(ket_1, ket_1.conj())
print(f"|0⟩⟨0| + |1⟩⟨1| = I?  {np.allclose(I_comp, np.eye(2))}")  # True

# Hadamard basis:
I_had = np.outer(ket_plus, ket_plus.conj()) + np.outer(ket_minus, ket_minus.conj())
print(f"|+⟩⟨+| + |−⟩⟨−| = I?  {np.allclose(I_had, np.eye(2))}")   # True

# Y-basis:
ket_plus_i = (ket_0 + 1j * ket_1) / np.sqrt(2)
ket_minus_i = (ket_0 - 1j * ket_1) / np.sqrt(2)
I_y = np.outer(ket_plus_i, ket_plus_i.conj()) + np.outer(ket_minus_i, ket_minus_i.conj())
print(f"|+i⟩⟨+i| + |−i⟩⟨−i| = I? {np.allclose(I_y, np.eye(2))}")  # True

# For 2-qubit computational basis:
basis_2q = [np.array([1,0,0,0], dtype=complex),
            np.array([0,1,0,0], dtype=complex),
            np.array([0,0,1,0], dtype=complex),
            np.array([0,0,0,1], dtype=complex)]
I_2q = sum(np.outer(b, b.conj()) for b in basis_2q)
print(f"\nΣ|ij⟩⟨ij| = I₄? {np.allclose(I_2q, np.eye(4))}")  # True

# Why does this matter? Because it guarantees probabilities sum to 1.
# P(0) + P(1) = ⟨ψ|0⟩⟨0|ψ⟩ + ⟨ψ|1⟩⟨1|ψ⟩ = ⟨ψ|(|0⟩⟨0| + |1⟩⟨1|)|ψ⟩ = ⟨ψ|I|ψ⟩ = ⟨ψ|ψ⟩ = 1
psi = np.array([0.6+0j, 0.8+0j])
p0 = abs(np.dot(ket_0.conj(), psi))**2
p1 = abs(np.dot(ket_1.conj(), psi))**2
print(f"\nP(0) = {p0:.4f}, P(1) = {p1:.4f}, Sum = {p0 + p1:.4f}")  # 1.0
