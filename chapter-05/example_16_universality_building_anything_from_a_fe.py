"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.8 Universality: Building Anything from a Few Gates
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_16_universality_building_anything_from_a_fe.py
"""

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# We can build ALL other standard gates from {H, T, CNOT}

# S = T² (two T gates)
S_built = T @ T
print(f"S from T²: {np.allclose(S_built, S)}")  # True

# Z = S² = T⁴
Z_built = T @ T @ T @ T
print(f"Z from T⁴: {np.allclose(Z_built, Z)}")  # True

# X = HZH = H·T⁴·H
X_built = H @ T @ T @ T @ T @ H
print(f"X from HT⁴H: {np.allclose(X_built, X)}")  # True

# T† (T-dagger, the inverse of T) = T⁷ (since T⁸ = I)
T_dag = T.conj().T
T7 = T @ T @ T @ T @ T @ T @ T
print(f"T† from T⁷: {np.allclose(T7, T_dag)}")  # True

# Verify: T⁸ = I (T has order 8)
T8 = np.eye(2, dtype=complex)
for _ in range(8):
    T8 = T8 @ T
print(f"T⁸ = I: {np.allclose(T8, np.eye(2))}")  # True
