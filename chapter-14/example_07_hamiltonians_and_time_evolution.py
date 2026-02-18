"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.2 Hamiltonians and Time Evolution
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_07_hamiltonians_and_time_evolution.py
"""

import numpy as np
from scipy.linalg import expm

# 2-qubit Hamiltonian: H = -Z⊗Z - 0.5*(X⊗I + I⊗X)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H_ZZ = -np.kron(Z, Z)
H_X  = -0.5 * (np.kron(X, I) + np.kron(I, X))
H = H_ZZ + H_X  # non-commuting terms

# Exact evolution
t = 1.0
U_exact = expm(-1j * H * t)

# Trotter approximation: (e^{-iH_ZZ dt} e^{-iH_X dt})^n
def trotter_evolve(H_terms, t, n_steps):
    dt = t / n_steps
    U_trotter = np.eye(H_terms[0].shape[0], dtype=complex)
    for _ in range(n_steps):
        for H_k in H_terms:
            U_trotter = expm(-1j * H_k * dt) @ U_trotter
    return U_trotter

# Compare Trotter error vs number of steps
print(f"{'Trotter steps':>14} | {'Operator error':>14} | {'Order'}")
print("-" * 50)
prev_err = None
for n in [1, 2, 4, 8, 16, 32, 64]:
    U_trot = trotter_evolve([H_ZZ, H_X], t, n)
    err = np.linalg.norm(U_trot - U_exact)
    order = ""
    if prev_err is not None and err > 1e-14:
        order = f"  ~1/{prev_err/err:.1f}"
    prev_err = err
    print(f"{n:>14} | {err:>14.8f} |{order}")
# Error scales as O(t²/n) for first-order Trotter -- halving the step
# roughly halves the error.
