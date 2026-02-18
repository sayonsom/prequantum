"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.1 The Pauli Gates: X, Y, Z
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_02_the_pauli_gates_x_y_z.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

# The three Pauli gates
X = np.array([[0, 1], [1, 0]], dtype=complex)      # NOT gate / bit flip
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)   # bit + phase flip
Z = np.array([[1, 0], [0, -1]], dtype=complex)      # phase flip

# X gate: flips |0⟩ ↔ |1⟩ (the classical NOT)
print("X gate (bit flip):")
print(f"  X|0⟩ = {X @ ket_0}  → |1⟩")
print(f"  X|1⟩ = {X @ ket_1}  → |0⟩")

# Z gate: flips the SIGN of |1⟩, leaves |0⟩ alone
print("\nZ gate (phase flip):")
print(f"  Z|0⟩ = {Z @ ket_0}  → |0⟩  (unchanged)")
print(f"  Z|1⟩ = {Z @ ket_1}  → -|1⟩ (sign flipped!)")

# Y gate: both a bit flip AND a phase flip (with factors of i)
print("\nY gate (bit + phase flip):")
print(f"  Y|0⟩ = {Y @ ket_0}  → i|1⟩")
print(f"  Y|1⟩ = {Y @ ket_1}  → -i|0⟩")
