"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_01_the_quick_win.py
"""

import numpy as np
from scipy.linalg import expm

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Heisenberg Hamiltonian for 2 spins: H = J(XX + YY + ZZ)
# J > 0: antiferromagnetic (spins prefer anti-alignment)
J = 1.0
H = J * (np.kron(X, X) + np.kron(Y, Y) + np.kron(Z, Z))

print("Heisenberg Hamiltonian (4x4):")
print(np.round(H.real, 2))

# Initial state: |↑↓⟩ = |01⟩ (first spin up, second spin down)
state_0 = np.array([0, 1, 0, 0], dtype=complex)

# Evolve and track probability of each basis state
print(f"\n{'t':>5}  P(|00⟩)  P(|01⟩)  P(|10⟩)  P(|11⟩)")
print("-" * 48)
for t in np.linspace(0, np.pi, 9):
    U = expm(-1j * H * t)
    psi = U @ state_0
    probs = np.abs(psi)**2
    print(f"{t:5.2f}  {probs[0]:7.4f}  {probs[1]:7.4f}  {probs[2]:7.4f}  {probs[3]:7.4f}")
# Output:
# Heisenberg Hamiltonian (4x4):
# [[ 1.  0.  0.  0.]
#  [ 0. -1.  2.  0.]
#  [ 0.  2. -1.  0.]
#  [ 0.  0.  0.  1.]]
#
#     t  P(|00⟩)  P(|01⟩)  P(|10⟩)  P(|11⟩)
# ------------------------------------------------
#  0.00   0.0000   1.0000   0.0000   0.0000
#  0.39   0.0000   0.6910   0.3090   0.0000
#  0.79   0.0000   0.0955   0.9045   0.0000
#  1.18   0.0000   0.0955   0.9045   0.0000
#  1.57   0.0000   0.6910   0.3090   0.0000
#  1.96   0.0000   1.0000   0.0000   0.0000
#  2.36   0.0000   0.6910   0.3090   0.0000
#  2.75   0.0000   0.0955   0.9045   0.0000
#  3.14   0.0000   0.6910   0.3090   0.0000
