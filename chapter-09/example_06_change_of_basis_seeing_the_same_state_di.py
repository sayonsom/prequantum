"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.4 Change of Basis: Seeing the Same State Differently
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_06_change_of_basis_seeing_the_same_state_di.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus_i = (ket_0 + 1j * ket_1) / np.sqrt(2)
ket_minus_i = (ket_0 - 1j * ket_1) / np.sqrt(2)

# Change-of-basis matrix for Y-basis
# Columns are Y-basis vectors expressed in computational basis
P_y = np.column_stack([ket_plus_i, ket_minus_i])
print(f"Y-basis change-of-basis matrix:")
print(np.round(P_y, 4))
# [[0.7071, 0.7071],
#  [0.7071j, -0.7071j]]  -- note the complex entries!

# This is NOT the Hadamard matrix -- it involves complex rotations.
# Verify it's unitary
print(f"\nP_y†P_y = I? {np.allclose(P_y.conj().T @ P_y, np.eye(2))}")  # True

# Convert |0⟩ to Y-basis coordinates
ket_0_in_y = P_y.conj().T @ ket_0
print(f"\n|0⟩ in Y-basis: {np.round(ket_0_in_y, 4)}")
# [0.7071, 0.7071] -- equal superposition of |+i⟩ and |−i⟩
# This means measuring |0⟩ in the Y-basis gives 50/50 results. Makes sense:
# |0⟩ is on the Z-axis of the Bloch sphere, equidistant from the Y-axis poles.
