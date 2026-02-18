"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.5 Gate Composition and the Order Trap
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_10_gate_composition_and_the_order_trap.py
"""

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

# Composing gates = matrix multiplication
# "Apply X then H" = H @ X (read right to left)
HX = H @ X
print(f"HX =\n{np.round(HX, 4)}")

# Key identities you can verify:
print(f"\nHXH = Z?  {np.allclose(H @ X @ H, Z)}")       # True!
print(f"HZH = X?  {np.allclose(H @ Z @ H, X)}")         # True!
print(f"SHS† = ?")
SHS_dag = S @ H @ S.conj().T
print(f"  {np.round(SHS_dag, 4)}")  # A rotation gate

# Every composition of unitary gates is also unitary
combo = T @ S @ H @ X @ Z
is_unitary = np.allclose(combo @ combo.conj().T, np.eye(2))
print(f"\nTSHXZ is unitary: {is_unitary}")  # True

# The inverse of a composition: (AB)† = B†A† (reverse order)
combo_inv = Z.conj().T @ X.conj().T @ H.conj().T @ S.conj().T @ T.conj().T
print(f"(TSHXZ)(TSHXZ)† = I: {np.allclose(combo @ combo_inv, np.eye(2))}")  # True
