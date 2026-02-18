"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.1 Eigenvalues and Eigenvectors: The Full Picture
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_04_eigenvalues_and_eigenvectors_the_full_pi.py
"""

import numpy as np

# Example: two commuting 4x4 matrices (2-qubit Z⊗I and I⊗Z)
I = np.eye(2, dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

A = np.kron(Z, I)  # Z on qubit 1
B = np.kron(I, Z)  # Z on qubit 2

commutator = A @ B - B @ A
print(f"[A, B] = 0? {np.allclose(commutator, 0)}")

# Both share the computational basis as eigenvectors
vals_A, vecs_A = np.linalg.eigh(A)
vals_B, vecs_B = np.linalg.eigh(B)

# A has degenerate eigenvalues: +1 (twice) and -1 (twice)
print(f"Eigenvalues of Z⊗I: {vals_A}")
print(f"Eigenvalues of I⊗Z: {vals_B}")
# Together they uniquely label each basis state:
# |00⟩: (+1, +1), |01⟩: (+1, -1), |10⟩: (-1, +1), |11⟩: (-1, -1)
for i in range(4):
    basis_state = np.zeros(4, dtype=complex)
    basis_state[i] = 1.0
    a_val = (basis_state.conj() @ A @ basis_state).real
    b_val = (basis_state.conj() @ B @ basis_state).real
    labels = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
    print(f"  {labels[i]}: Z⊗I → {a_val:+.0f}, I⊗Z → {b_val:+.0f}")
# Output:
# [A, B] = 0? True
# Eigenvalues of Z⊗I: [-1. -1.  1.  1.]
# Eigenvalues of I⊗Z: [-1.  1. -1.  1.]
#   |00⟩: Z⊗I → +1, I⊗Z → +1
#   |01⟩: Z⊗I → +1, I⊗Z → -1
#   |10⟩: Z⊗I → -1, I⊗Z → +1
#   |11⟩: Z⊗I → -1, I⊗Z → -1
