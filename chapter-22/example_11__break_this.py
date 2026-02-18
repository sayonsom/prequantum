"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 4: The AI Lab > 🐛 Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_11__break_this.py
"""

import numpy as np

# Pauli matrices
I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])

# Encoded |0⟩_L = |000⟩
state = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=float)

# Stabilizers
S1 = np.kron(np.kron(Z, Z), I)  # Z₀Z₁
S2 = np.kron(np.kron(I, Z), Z)  # Z₁Z₂

# Bug 1: wrong error operator
# Trying to apply X error on qubit 1
error = np.kron(np.kron(I, X), I)
state_error = error @ state

# Bug 2: checking syndrome wrong
syndrome_1 = state_error @ S1 @ state_error  # this gives a NUMBER
syndrome_2 = state_error @ S2 @ state_error
print(f"Syndrome: ({syndrome_1}, {syndrome_2})")

# Apply "correction"
if syndrome_1 == -1 and syndrome_2 == -1:
    correction = np.kron(np.kron(I, X), I)
    state_corrected = correction @ state_error
    print(f"Corrected! Final state matches original: {np.allclose(state_corrected, state)}")
