"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_11_break_this.py
"""

import numpy as np
from scipy.linalg import expm

X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Hamiltonian: H = X (a single-term Hamiltonian)
H = X
t = np.pi / 2
state = np.array([1, 0], dtype=complex)

# "Trotterize" H = X by splitting into Z + (X - Z)
# BUG: This decomposition is pointless and introduces unnecessary error!
H1 = Z
H2 = X - Z  # This is NOT a standard Pauli term

n_steps = 100
dt = t / n_steps
evolved = state.copy()
for _ in range(n_steps):
    evolved = expm(-1j * H1 * dt) @ expm(-1j * H2 * dt) @ evolved

exact = expm(-1j * H * t) @ state
print(f"Exact:   {np.round(exact, 4)}")
print(f"Trotter: {np.round(evolved, 4)}")
print(f"Error:   {np.linalg.norm(evolved - exact):.6f}")
