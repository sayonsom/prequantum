"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_13_break_this.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 + ket_1) / np.sqrt(2)  # BUG: should be ket_0 - ket_1

print(f"⟨+|+⟩ = {np.dot(ket_plus.conj(), ket_plus):.4f}")   # Should be 1
print(f"⟨−|−⟩ = {np.dot(ket_minus.conj(), ket_minus):.4f}")  # Should be 1
print(f"⟨+|−⟩ = {np.dot(ket_plus.conj(), ket_minus):.4f}")   # Should be 0, prints 1!
