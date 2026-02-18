"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.10 Putting It All Together: The Gate Landscape
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_19_putting_it_all_together_the_gate_landsca.py
"""

import numpy as np

# === The complete single-qubit gate landscape ===

def Rz(theta):
    return np.array([[np.exp(-1j*theta/2), 0], [0, np.exp(1j*theta/2)]], dtype=complex)

def Rx(theta):
    return np.array([
        [np.cos(theta/2), -1j*np.sin(theta/2)],
        [-1j*np.sin(theta/2), np.cos(theta/2)]
    ], dtype=complex)

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

# Key relationships to internalize:
print("=== Gate Relationships ===")

# Pauli gates as π-rotations
print(f"\nRx(π) ≈ -iX? {np.allclose(Rx(np.pi), -1j * X)}")  # True
print(f"Rz(π) ≈ -iZ? {np.allclose(Rz(np.pi), -1j * Z)}")  # True

# Conjugation identities (H swaps X ↔ Z)
print(f"\nHXH = Z? {np.allclose(H @ X @ H, Z)}")  # True
print(f"HZH = X? {np.allclose(H @ Z @ H, X)}")  # True
print(f"HYH = -Y? {np.allclose(H @ Y @ H, -Y)}")  # True

# Phase gate hierarchy
print(f"\nT² = S? {np.allclose(T @ T, S)}")  # True
print(f"S² = Z? {np.allclose(S @ S, Z)}")  # True
print(f"T⁸ = I? {np.allclose(np.linalg.matrix_power(T, 8), np.eye(2))}")  # True

# The Rx gate: rotations around x-axis
print(f"\nRx(π/2):")
print(np.round(Rx(np.pi/2), 4))
print(f"Is unitary? {np.allclose(Rx(np.pi/2) @ Rx(np.pi/2).conj().T, np.eye(2))}")

# Any single-qubit gate can be decomposed as Rz(α)·Rx(β)·Rz(γ)
# (the ZXZ decomposition / Euler angles)
# This means Rz and Rx together are universal for single-qubit gates!
alpha, beta, gamma = np.pi/3, np.pi/5, np.pi/7
arbitrary_1q = Rz(alpha) @ Rx(beta) @ Rz(gamma)
print(f"\nRz·Rx·Rz is unitary? {np.allclose(arbitrary_1q @ arbitrary_1q.conj().T, np.eye(2))}")
