"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.1 The Simulation Problem
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_02_the_simulation_problem.py
"""

import numpy as np
from scipy.linalg import expm

# Hamiltonians we CAN easily implement as gates:
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# e^{-i theta Z} is a Rz gate (easy!)
theta = 0.5
Rz = expm(-1j * theta * Z)
print("e^{-iθZ} (a rotation gate):")
print(np.round(Rz, 4))
print(f"Is it diagonal? {np.allclose(Rz, np.diag(np.diag(Rz)))}")

# e^{-i theta ZZ} is also implementable (CNOT + Rz + CNOT)
ZZ = np.kron(Z, Z)
U_zz = expm(-1j * theta * ZZ)
print(f"\ne^{{-iθ(Z⊗Z)}} diagonal? {np.allclose(U_zz, np.diag(np.diag(U_zz)))}")

# But e^{-i theta (XX + YY + ZZ)} is NOT simply decomposable
H_full = np.kron(X, X) + np.kron(Y, Y) + np.kron(Z, Z)
U_full = expm(-1j * theta * H_full)
print(f"\ne^{{-iθ(XX+YY+ZZ)}} diagonal? {np.allclose(U_full, np.diag(np.diag(U_full)))}")
print("This one needs Trotterization...")
# Output:
# e^{-iθZ} (a rotation gate):
# [[0.8776-0.4794j 0.    +0.j    ]
#  [0.    +0.j     0.8776+0.4794j]]
# Is it diagonal? True
#
# e^{-iθ(Z⊗Z)} diagonal? True
#
# e^{-iθ(XX+YY+ZZ)} diagonal? False
# This one needs Trotterization...
