"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.3 The General Phase Gate: Rz(θ)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_08_the_general_phase_gate_rzθ.py
"""

import numpy as np

def P_gate(theta):
    """Phase gate: adds phase theta to |1⟩, leaves |0⟩ alone."""
    return np.array([[1, 0], [0, np.exp(1j * theta)]], dtype=complex)

def Rz(theta):
    return np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)]
    ], dtype=complex)

# P(θ) and Rz(θ) differ only by a global phase
theta = np.pi / 3
P = P_gate(theta)
R = Rz(theta)

# They give different state vectors...
ket_0 = np.array([1, 0], dtype=complex)
print(f"P(π/3)|0⟩  = {np.round(P @ ket_0, 4)}")   # [1, 0]
print(f"Rz(π/3)|0⟩ = {np.round(R @ ket_0, 4)}")    # [e^(-iπ/6), 0]

# ...but identical measurement probabilities
state_P = P @ (ket_0 + np.array([0, 1])) / np.sqrt(2)
state_R = R @ (ket_0 + np.array([0, 1])) / np.sqrt(2)
print(f"\nP(π/3)|+⟩ probs:  {np.round(np.abs(state_P)**2, 4)}")
print(f"Rz(π/3)|+⟩ probs: {np.round(np.abs(state_R)**2, 4)}")
# Same probabilities!
