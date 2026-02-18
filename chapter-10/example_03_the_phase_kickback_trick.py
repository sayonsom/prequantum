"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.2 The Phase Kickback Trick
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_03_the_phase_kickback_trick.py
"""

import numpy as np

# Phase kickback: the output qubit in |−⟩ turns the oracle into a phase oracle
# U_f|x⟩|−⟩ = (-1)^f(x) |x⟩|−⟩

# Proof:
# |−⟩ = (|0⟩ − |1⟩)/√2
# U_f|x⟩|−⟩ = U_f|x⟩(|0⟩ − |1⟩)/√2
#            = |x⟩(|0 ⊕ f(x)⟩ − |1 ⊕ f(x)⟩)/√2
#
# If f(x) = 0: (|0⟩ − |1⟩)/√2 = |−⟩  → phase = +1
# If f(x) = 1: (|1⟩ − |0⟩)/√2 = -|−⟩ → phase = -1
#
# So: U_f|x⟩|−⟩ = (-1)^f(x) |x⟩|−⟩
# The output qubit is UNCHANGED. The phase goes to the INPUT register!

# Let's verify numerically for f(x) = x (identity function, 1-bit)
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

# Input: |0⟩|−⟩ → f(0) = 0, so phase = +1
state_0_minus = np.kron(ket_0, ket_minus)
result_0 = CNOT @ state_0_minus
expected_0 = (+1) * np.kron(ket_0, ket_minus)
print(f"|0⟩|−⟩ after oracle: phase = +1? {np.allclose(result_0, expected_0)}")

# Input: |1⟩|−⟩ → f(1) = 1, so phase = -1
state_1_minus = np.kron(ket_1, ket_minus)
result_1 = CNOT @ state_1_minus
expected_1 = (-1) * np.kron(ket_1, ket_minus)
print(f"|1⟩|−⟩ after oracle: phase = -1? {np.allclose(result_1, expected_1)}")

# Input: |+⟩|−⟩ → superposition picks up different phases!
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
state_plus_minus = np.kron(ket_plus, ket_minus)
result_plus = CNOT @ state_plus_minus
print(f"\n|+⟩|−⟩ after oracle:")
print(f"  Result: {np.round(result_plus, 4)}")
# Should be ((+1)|0⟩ + (-1)|1⟩)/√2 ⊗ |−⟩ = |−⟩ ⊗ |−⟩
expected_plus = np.kron(ket_minus, ket_minus)
print(f"  = |−⟩|−⟩? {np.allclose(result_plus, expected_plus)}")
