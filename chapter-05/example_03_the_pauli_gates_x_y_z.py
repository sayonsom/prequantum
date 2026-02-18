"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.1 The Pauli Gates: X, Y, Z
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_03_the_pauli_gates_x_y_z.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Z on |0⟩ or |1⟩: probabilities unchanged
state = Z @ ket_0
print(f"Z|0⟩: P(0)={abs(state[0])**2:.2f}, P(1)={abs(state[1])**2:.2f}")
# P(0)=1.00, P(1)=0.00 -- same as before Z

# Z on |+⟩: probabilities change!
state = Z @ ket_plus
print(f"Z|+⟩ = {np.round(state, 4)}")
# [0.7071, -0.7071] → that's |−⟩!
print(f"Z|+⟩ = |−⟩? {np.allclose(state, ket_minus)}")  # True
