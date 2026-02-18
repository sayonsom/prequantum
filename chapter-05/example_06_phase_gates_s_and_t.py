"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.2 Phase Gates: S and T
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_06_phase_gates_s_and_t.py
"""

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
S = np.array([[1, 0], [0, np.exp(1j * np.pi / 2)]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
ket_0 = np.array([1, 0], dtype=complex)

# Phase gates sandwiched between Hadamards create different biases
for name, gate in [("I (none)", np.eye(2)), ("T", T), ("S", S), ("Z", Z)]:
    state = H @ gate @ H @ ket_0
    p0 = abs(state[0])**2
    p1 = abs(state[1])**2
    print(f"  H·{name:8s}·H|0⟩: P(0)={p0:.4f}, P(1)={p1:.4f}")
# H·I       ·H|0⟩: P(0)=1.0000, P(1)=0.0000  ← HH = I, back to |0⟩
# H·T       ·H|0⟩: P(0)=0.8536, P(1)=0.1464  ← biased ~85/15
# H·S       ·H|0⟩: P(0)=0.5000, P(1)=0.5000  ← 50/50 (but different from H alone!)
# H·Z       ·H|0⟩: P(0)=0.0000, P(1)=1.0000  ← certainty! HZH = X
