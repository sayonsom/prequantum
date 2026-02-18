"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.4 Eigenvalues and Phase Estimation
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_05_eigenvalues_and_phase_estimation.py
"""

import numpy as np

# Eigenvalues: U|u⟩ = λ|u⟩
# For unitary matrices, eigenvalues have |λ| = 1, so λ = e^(2πiφ)

# Example: Pauli Z gate
Z = np.array([[1, 0], [0, -1]], dtype=complex)
eigenvalues, eigenvectors = np.linalg.eig(Z)

print("Z gate eigenvalues and eigenvectors:")
for i, (val, vec) in enumerate(zip(eigenvalues, eigenvectors.T)):
    phase = np.angle(val) / (2 * np.pi)
    print(f"  λ_{i} = {val:+.4f} = e^(2πi·{phase:.4f}), "
          f"|u_{i}⟩ = {np.round(vec, 4)}")

# Phase gate S: eigenvalues are 1 and i = e^(2πi/4)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
eigenvalues_S, eigenvectors_S = np.linalg.eig(S)

print(f"\nS gate eigenvalues:")
for i, (val, vec) in enumerate(zip(eigenvalues_S, eigenvectors_S.T)):
    phase = np.angle(val) / (2 * np.pi)
    print(f"  λ_{i} = {val}, phase φ = {phase:.4f}, |u_{i}⟩ = {np.round(vec, 4)}")

# T gate: eigenvalues are 1 and e^(iπ/4) = e^(2πi/8)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
eigenvalues_T, eigenvectors_T = np.linalg.eig(T)

print(f"\nT gate eigenvalues:")
for i, (val, vec) in enumerate(zip(eigenvalues_T, eigenvectors_T.T)):
    phase = np.angle(val) / (2 * np.pi)
    print(f"  λ_{i} = {val:.4f}, phase φ = {phase:.4f}")
