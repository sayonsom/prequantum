"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.10 The Spectral Decomposition: Putting It All Together
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_13_the_spectral_decomposition_putting_it_al.py
"""

import numpy as np

# ─── SPECTRAL DECOMPOSITION OF PAULI Z ───
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eigh(Z)
print(f"Z eigenvalues: {eigenvalues}")  # [-1, 1]

# Reconstruct Z from eigenvalues and projectors
v0 = eigenvectors[:, 0]  # eigenvector for λ=-1 → |1⟩
v1 = eigenvectors[:, 1]  # eigenvector for λ=+1 → |0⟩
Z_reconstructed = eigenvalues[0] * np.outer(v0, v0.conj()) + \
                  eigenvalues[1] * np.outer(v1, v1.conj())
print(f"\nZ reconstructed from spectral decomposition:")
print(np.round(Z_reconstructed.real, 4))
print(f"Matches original? {np.allclose(Z, Z_reconstructed)}")  # True

# ─── SPECTRAL DECOMPOSITION OF PAULI X ───
X = np.array([[0, 1], [1, 0]], dtype=complex)
eigenvalues_X, eigenvectors_X = np.linalg.eigh(X)
X_reconstructed = sum(lam * np.outer(v, v.conj())
                      for lam, v in zip(eigenvalues_X, eigenvectors_X.T))
print(f"\nX reconstructed? {np.allclose(X, X_reconstructed)}")  # True

# ─── WHY THIS MATTERS: MEASUREMENT AS SPECTRAL DECOMPOSITION ───
# When you measure observable A on state |ψ⟩:
# - Possible outcomes: eigenvalues λᵢ
# - Probability of λᵢ: |⟨eᵢ|ψ⟩|²
# - Post-measurement state if you get λᵢ: |eᵢ⟩
# - Expected value: ⟨ψ|A|ψ⟩ = Σᵢ λᵢ |⟨eᵢ|ψ⟩|²

psi = np.array([0.6+0j, 0.8+0j])
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Expected value of Z measurement
expectation_Z = np.dot(psi.conj(), Z @ psi).real
# Same thing manually: (+1)|⟨0|ψ⟩|² + (-1)|⟨1|ψ⟩|²
manual = (+1) * abs(np.dot(ket_0.conj(), psi))**2 + \
         (-1) * abs(np.dot(ket_1.conj(), psi))**2
print(f"\n⟨ψ|Z|ψ⟩ = {expectation_Z:.4f}")
print(f"Manual:  = {manual:.4f}")
print(f"Match? {np.allclose(expectation_Z, manual)}")  # True
# Expected Z = 0.36 - 0.64 = -0.28 (biased toward |1⟩, as expected for state 0.6|0⟩ + 0.8|1⟩)
