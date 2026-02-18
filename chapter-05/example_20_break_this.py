"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_20_break_this.py
"""

import numpy as np

CNOT_01 = np.array([  # control=q0, target=q1
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

# BUG: This is the same CNOT, not the reversed one!
# Should be control=q1, target=q0
CNOT_10 = np.array([  # WRONG: still control=q0, target=q1
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

SWAP_expected = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
], dtype=complex)

SWAP_attempt = CNOT_01 @ CNOT_10 @ CNOT_01
print(f"SWAP from 3 CNOTs? {np.allclose(SWAP_attempt, SWAP_expected)}")
# Prints False! The middle CNOT needs reversed control/target.
