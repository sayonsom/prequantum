"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.7 Multi-Qubit Gates: CNOT, Toffoli, SWAP
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_13_multi_qubit_gates_cnot_toffoli_swap.py
"""

import numpy as np

CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

# Verify it's unitary
print(f"CNOT is unitary: {np.allclose(CNOT @ CNOT.conj().T, np.eye(4))}")  # True

# CNOT is its own inverse (like the Pauli gates)
print(f"CNOT² = I: {np.allclose(CNOT @ CNOT, np.eye(4))}")  # True
