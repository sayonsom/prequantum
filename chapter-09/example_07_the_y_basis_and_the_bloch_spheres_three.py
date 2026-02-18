"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.5 The Y-Basis and the Bloch Sphere's Three Axes
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_07_the_y_basis_and_the_bloch_spheres_three.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Y-basis: eigenvectors of the Pauli Y gate
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

# Compute eigenvectors
eigenvalues, eigenvectors = np.linalg.eigh(Y)  # eigh for Hermitian matrices
print(f"Y eigenvalues: {np.round(eigenvalues, 4)}")  # [-1, +1]

# The Y-basis vectors (conventionally written as |+i⟩ and |−i⟩)
ket_plus_i = (ket_0 + 1j * ket_1) / np.sqrt(2)   # eigenvalue +1
ket_minus_i = (ket_0 - 1j * ket_1) / np.sqrt(2)  # eigenvalue -1

# Verify they're Y eigenvectors
print(f"\nY|+i⟩ = {np.round(Y @ ket_plus_i, 4)}")
print(f"|+i⟩   = {np.round(ket_plus_i, 4)}")
print(f"Eigenvalue +1? {np.allclose(Y @ ket_plus_i, ket_plus_i)}")  # True

# Verify orthonormality
print(f"\n⟨+i|−i⟩ = {np.dot(ket_plus_i.conj(), ket_minus_i):.4f}")  # 0
print(f"⟨+i|+i⟩ = {np.dot(ket_plus_i.conj(), ket_plus_i):.4f}")   # 1

# Three bases, three measurement directions:
# Z-basis {|0⟩, |1⟩}:     measures spin along Z-axis of Bloch sphere
# X-basis {|+⟩, |−⟩}:     measures spin along X-axis
# Y-basis {|+i⟩, |−i⟩}:   measures spin along Y-axis
# Together they span all three spatial directions.

# Express |0⟩ in each basis:
print(f"\n|0⟩ in Z-basis: 1.0|0⟩ + 0.0|1⟩")
print(f"|0⟩ in X-basis: {np.dot(ket_plus_i.conj(), ket_0):.4f}|+i⟩ + "
      f"{np.dot(ket_minus_i.conj(), ket_0):.4f}|−i⟩")
# 50/50 in Y-basis -- measuring |0⟩ in Y gives random results
