"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.2 Trotterization: Breaking the Exponential Apart
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_03_trotterization_breaking_the_exponential.py
"""

import numpy as np
from scipy.linalg import expm

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Heisenberg Hamiltonian: H = XX + YY + ZZ
H_xx = np.kron(X, X)
H_yy = np.kron(Y, Y)
H_zz = np.kron(Z, Z)
H = H_xx + H_yy + H_zz

t = 1.0  # simulation time

# Exact evolution
U_exact = expm(-1j * H * t)

# First-order Trotter: e^{-iHt} ≈ (e^{-i H_xx dt} e^{-i H_yy dt} e^{-i H_zz dt})^n
def trotter_first_order(t, n_steps):
    dt = t / n_steps
    U = np.eye(4, dtype=complex)
    for _ in range(n_steps):
        U = expm(-1j * H_xx * dt) @ expm(-1j * H_yy * dt) @ expm(-1j * H_zz * dt) @ U
    return U

# Second-order Trotter (Suzuki): symmetric splitting
# e^{-iHt} ≈ (e^{-i H_xx dt/2} e^{-i H_yy dt/2} e^{-i H_zz dt}
#              e^{-i H_yy dt/2} e^{-i H_xx dt/2})^n
def trotter_second_order(t, n_steps):
    dt = t / n_steps
    U = np.eye(4, dtype=complex)
    for _ in range(n_steps):
        U = (expm(-1j * H_xx * dt/2)
             @ expm(-1j * H_yy * dt/2)
             @ expm(-1j * H_zz * dt)
             @ expm(-1j * H_yy * dt/2)
             @ expm(-1j * H_xx * dt/2)) @ U
    return U

# Compare errors for different step counts
print(f"{'n_steps':>8}  {'1st-order error':>16}  {'2nd-order error':>16}  {'ratio_1st':>10}  {'ratio_2nd':>10}")
print("-" * 68)
prev_err1, prev_err2 = None, None
for n in [1, 2, 4, 8, 16, 32, 64]:
    U1 = trotter_first_order(t, n)
    U2 = trotter_second_order(t, n)
    err1 = np.linalg.norm(U1 - U_exact)
    err2 = np.linalg.norm(U2 - U_exact)
    r1 = f"{prev_err1/err1:.2f}" if prev_err1 else "---"
    r2 = f"{prev_err2/err2:.2f}" if prev_err2 else "---"
    print(f"{n:>8}  {err1:>16.8f}  {err2:>16.8f}  {r1:>10}  {r2:>10}")
    prev_err1, prev_err2 = err1, err2
# Output:
#  n_steps  1st-order error  2nd-order error   ratio_1st   ratio_2nd
# --------------------------------------------------------------------
#        1      1.59498138      0.53545852         ---         ---
#        2      0.73610699      0.10816073        2.17        4.95
#        4      0.35220131      0.02423399        2.09        4.46
#        8      0.17240430      0.00584825        2.04        4.14
#       16      0.08545488      0.00144690        2.02        4.04
#       32      0.04256017      0.00036023        2.01        4.02
#       64      0.02124528      0.00008998        2.00        4.00
