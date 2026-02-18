"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.1 Eigenvalues and Eigenvectors: The Full Picture
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_03_eigenvalues_and_eigenvectors_the_full_pi.py
"""

import numpy as np

# Spectral decomposition of Pauli-Z
Z = np.array([[1, 0], [0, -1]], dtype=complex)
eigenvalues, eigenvectors = np.linalg.eig(Z)

# Reconstruct Z from its eigendecomposition
Z_reconstructed = sum(
    eigenvalues[i] * np.outer(eigenvectors[:, i], eigenvectors[:, i].conj())
    for i in range(len(eigenvalues))
)

print("Original Z:")
print(Z)
print("\nReconstructed from eigendecomposition:")
print(np.round(Z_reconstructed, 4))
print(f"\nMatch: {np.allclose(Z, Z_reconstructed)}")
# Output:
# Original Z:
# [[ 1.+0.j  0.+0.j]
#  [ 0.+0.j -1.+0.j]]
#
# Reconstructed from eigendecomposition:
# [[ 1.+0.j  0.+0.j]
#  [ 0.+0.j -1.+0.j]]
#
# Match: True
