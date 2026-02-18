"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.8 Hermitian Matrices: What You Can Measure
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_11_hermitian_matrices_what_you_can_measure.py
"""

import numpy as np

# ─── CONJUGATE TRANSPOSE (DAGGER) ───
A = np.array([[1+2j, 3+4j],
              [5+6j, 7+8j]])
A_dagger = A.conj().T
print(f"A =\n{A}")
print(f"\nA† =\n{A_dagger}")
# Transpose: rows ↔ columns. Conjugate: flip sign of imaginary parts.

# ─── HERMITIAN MATRICES: A† = A ───
# These represent OBSERVABLES (things you can measure)
Z_gate = np.array([[1, 0], [0, -1]], dtype=complex)  # Pauli Z
print(f"\nZ gate:\n{Z_gate}")
print(f"Z† = Z? {np.allclose(Z_gate.conj().T, Z_gate)}")  # True → Hermitian

X_gate = np.array([[0, 1], [1, 0]], dtype=complex)  # Pauli X
print(f"X† = X? {np.allclose(X_gate.conj().T, X_gate)}")  # True → Hermitian

Y_gate = np.array([[0, -1j], [1j, 0]], dtype=complex)  # Pauli Y
print(f"Y† = Y? {np.allclose(Y_gate.conj().T, Y_gate)}")  # True → Hermitian

H_gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
print(f"H† = H? {np.allclose(H_gate.conj().T, H_gate)}")  # True → Hermitian

# Hermitian matrices have REAL eigenvalues (always)
eigenvalues_Z = np.linalg.eigvalsh(Z_gate)
eigenvalues_X = np.linalg.eigvalsh(X_gate)
eigenvalues_Y = np.linalg.eigvalsh(Y_gate)
print(f"\nZ eigenvalues: {eigenvalues_Z}")  # [-1, 1] -- real numbers
print(f"X eigenvalues: {eigenvalues_X}")  # [-1, 1]
print(f"Y eigenvalues: {eigenvalues_Y}")  # [-1, 1]
# All three Pauli matrices have the same eigenvalues: ±1
# These are the possible measurement outcomes.
