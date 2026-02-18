"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.2 Applying Gates to Multi-Qubit Systems
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_06_applying_gates_to_multi_qubit_systems.py
"""

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)  # Hadamard
I = np.eye(2, dtype=complex)  # Identity: does nothing

# "Apply H to qubit 0, do nothing to qubit 1"
H_on_q0 = np.kron(H, I)  # 4x4 matrix

# "Do nothing to qubit 0, apply H to qubit 1"
H_on_q1 = np.kron(I, H)  # 4x4 matrix

# Apply H to qubit 0 in a two-qubit system
state = np.array([1, 0, 0, 0], dtype=complex)  # |00>
new_state = H_on_q0 @ state
print(f"After H on q0: {np.round(new_state, 4)}")
# [0.7071, 0, 0.7071, 0] -> superposition of "00" and "10"
