"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_01_the_quick_win.py
"""

import numpy as np
from scipy.linalg import expm

# Pauli-Z as the Hamiltonian
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Initial state: |+⟩
state = np.array([1, 1], dtype=complex) / np.sqrt(2)

# Time evolution: |ψ(t)⟩ = e^{-iHt} |ψ(0)⟩
print("Time | Prob(|0⟩) | Prob(|1⟩)")
print("-" * 35)
for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
    U = expm(-1j * Z * t)           # time evolution operator
    evolved = U @ state
    p0 = abs(evolved[0])**2
    p1 = abs(evolved[1])**2
    print(f" {t:.2f} |   {p0:.4f}   |   {p1:.4f}")
# Output:
# Time | Prob(|0⟩) | Prob(|1⟩)
# -----------------------------------
#  0.00 |   0.5000   |   0.5000
#  0.25 |   0.5000   |   0.5000
#  0.50 |   0.5000   |   0.5000
#  0.75 |   0.5000   |   0.5000
#  1.00 |   0.5000   |   0.5000
