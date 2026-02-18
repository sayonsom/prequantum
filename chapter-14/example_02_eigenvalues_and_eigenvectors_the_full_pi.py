"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.1 Eigenvalues and Eigenvectors: The Full Picture
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_02_eigenvalues_and_eigenvectors_the_full_pi.py
"""

import numpy as np

# The Pauli-X matrix (bit-flip gate)
X = np.array([[0, 1], [1, 0]], dtype=complex)

# Find eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(X)

for i in range(len(eigenvalues)):
    val = eigenvalues[i]
    vec = eigenvectors[:, i]  # columns are eigenvectors
    # Verify: X @ vec == val * vec
    lhs = X @ vec
    rhs = val * vec
    print(f"Eigenvalue λ = {val.real:+.1f}")
    print(f"  Eigenvector: {np.round(vec, 4)}")
    print(f"  X @ vec:     {np.round(lhs, 4)}")
    print(f"  λ * vec:     {np.round(rhs, 4)}")
    print(f"  Match: {np.allclose(lhs, rhs)}")
    print()
# Output:
# Eigenvalue λ = +1.0
#   Eigenvector: [0.7071 0.7071]
#   X @ vec:     [0.7071 0.7071]
#   λ * vec:     [0.7071 0.7071]
#   Match: True
#
# Eigenvalue λ = -1.0
#   Eigenvector: [-0.7071  0.7071]
#   X @ vec:     [ 0.7071 -0.7071]
#   λ * vec:     [ 0.7071 -0.7071]
#   Match: True
