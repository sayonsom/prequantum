"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.4 The Hadamard Revisited: Basis Change
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_09_the_hadamard_revisited_basis_change.py
"""

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

# H converts between bases
print("Computational → Hadamard:")
print(f"  H|0⟩ = |+⟩? {np.allclose(H @ ket_0, ket_plus)}")    # True
print(f"  H|1⟩ = |−⟩? {np.allclose(H @ ket_1, ket_minus)}")   # True

print("\nHadamard → Computational:")
print(f"  H|+⟩ = |0⟩? {np.allclose(H @ ket_plus, ket_0)}")    # True
print(f"  H|−⟩ = |1⟩? {np.allclose(H @ ket_minus, ket_1)}")   # True

# H is its own inverse: H† = H, and H² = I
print(f"\nH = H†? {np.allclose(H, H.conj().T)}")  # True
print(f"H² = I? {np.allclose(H @ H, np.eye(2))}")  # True
