"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_01_the_quick_win.py
"""

import numpy as np

# States you built in Chapter 3, now with their physics names
ket_0 = np.array([1, 0], dtype=complex)    # |0⟩
ket_1 = np.array([0, 1], dtype=complex)    # |1⟩
ket_plus = (ket_0 + ket_1) / np.sqrt(2)    # |+⟩

# The "braket" -- inner product of two states
braket_00 = np.dot(ket_0.conj(), ket_0)
braket_01 = np.dot(ket_0.conj(), ket_1)
braket_0plus = np.dot(ket_0.conj(), ket_plus)

print(f"⟨0|0⟩ = {braket_00}")               # 1 -- same state, full overlap
print(f"⟨0|1⟩ = {braket_01}")               # 0 -- orthogonal, zero overlap
print(f"⟨0|+⟩ = {braket_0plus:.4f}")        # 0.7071
print(f"|⟨0|+⟩|² = {abs(braket_0plus)**2:.4f}")  # 0.5 -- probability!
