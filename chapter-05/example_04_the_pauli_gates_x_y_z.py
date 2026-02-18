"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.1 The Pauli Gates: X, Y, Z
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_04_the_pauli_gates_x_y_z.py
"""

import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Each Pauli squared = identity
print(f"X² = I? {np.allclose(X @ X, np.eye(2))}")  # True
print(f"Y² = I? {np.allclose(Y @ Y, np.eye(2))}")  # True
print(f"Z² = I? {np.allclose(Z @ Z, np.eye(2))}")  # True

# In notation: X² = Y² = Z² = I
# Also: XYZ = iI (they're related by multiplication too)
print(f"\nXYZ = iI? {np.allclose(X @ Y @ Z, 1j * np.eye(2))}")  # True
