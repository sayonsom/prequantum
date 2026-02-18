"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.2 Hamiltonians and Time Evolution
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_05_hamiltonians_and_time_evolution.py
"""

import numpy as np
from scipy.linalg import expm

# Hamiltonian: X gate (models a qubit in a transverse magnetic field)
X = np.array([[0, 1], [1, 0]], dtype=complex)
H = X  # energy scale = 1

# Initial state: |0⟩
state_0 = np.array([1, 0], dtype=complex)

# Evolve over time and track probabilities
times = np.linspace(0, np.pi, 9)
print("  t/π  | Prob(|0⟩) | Prob(|1⟩)")
print("-" * 37)
for t in times:
    U_t = expm(-1j * H * t)          # time evolution operator
    psi_t = U_t @ state_0
    p0 = abs(psi_t[0])**2
    p1 = abs(psi_t[1])**2
    print(f" {t/np.pi:.3f} |   {p0:.4f}   |   {p1:.4f}")
# Output:
#   t/π  | Prob(|0⟩) | Prob(|1⟩)
# -------------------------------------
#  0.000 |   1.0000   |   0.0000
#  0.125 |   0.8536   |   0.1464
#  0.250 |   0.5000   |   0.5000
#  0.375 |   0.1464   |   0.8536
#  0.500 |   0.0000   |   1.0000
#  0.625 |   0.1464   |   0.8536
#  0.750 |   0.5000   |   0.5000
#  0.875 |   0.8536   |   0.1464
#  1.000 |   1.0000   |   0.0000
