"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.7 Multi-Qubit Gates: CNOT, Toffoli, SWAP
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_14_multi_qubit_gates_cnot_toffoli_swap.py
"""

import numpy as np

SWAP = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
], dtype=complex)

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# SWAP |01⟩ = |10⟩
state_01 = np.kron(ket_0, ket_1)
state_10 = np.kron(ket_1, ket_0)
result = SWAP @ state_01
print(f"SWAP|01⟩ = {result}")  # [0, 0, 1, 0] = |10⟩
print(f"Equals |10⟩? {np.allclose(result, state_10)}")  # True

# SWAP is built from three CNOTs
CNOT_01 = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
# CNOT_reversed: control=qubit1, target=qubit0
CNOT_10 = np.array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0]
], dtype=complex)

SWAP_from_cnots = CNOT_01 @ CNOT_10 @ CNOT_01
print(f"\n3 CNOTs = SWAP? {np.allclose(SWAP_from_cnots, SWAP)}")  # True
