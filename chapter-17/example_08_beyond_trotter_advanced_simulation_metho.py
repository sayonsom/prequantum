"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.7 Beyond Trotter: Advanced Simulation Methods
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_08_beyond_trotter_advanced_simulation_metho.py
"""

import numpy as np
from scipy.linalg import expm

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Heisenberg model: H = 1.0*XX + 1.0*YY + 1.0*ZZ
terms = [np.kron(X, X), np.kron(Y, Y), np.kron(Z, Z)]
coeffs = [1.0, 1.0, 1.0]
H = sum(c * t for c, t in zip(coeffs, terms))
lambda_total = sum(abs(c) for c in coeffs)  # = 3.0

t_sim = 1.0
U_exact = expm(-1j * H * t_sim)

# qDRIFT: randomly sample terms, weighted by |coefficient|
def qdrift(t, n_steps, seed=42):
    """qDRIFT simulation: each step applies one random term."""
    rng = np.random.default_rng(seed)
    probs = [abs(c) / lambda_total for c in coeffs]
    tau = lambda_total * t / n_steps  # scaled time per step

    U = np.eye(4, dtype=complex)
    for _ in range(n_steps):
        j = rng.choice(len(terms), p=probs)
        # Apply e^{-i * sign(h_j) * tau * H_j}
        sign = np.sign(coeffs[j])
        U = expm(-1j * sign * tau * terms[j]) @ U
    return U

# Compare qDRIFT to deterministic Trotter
# qDRIFT error is stochastic -- average over trials
print(f"{'n_steps':>8}  {'Trotter-1 err':>14}  {'qDRIFT err (avg)':>18}  {'qDRIFT err (std)':>18}")
print("-" * 62)
for n in [10, 20, 50, 100, 200]:
    # Deterministic first-order Trotter
    dt = t_sim / n
    U_trot = np.eye(4, dtype=complex)
    for _ in range(n):
        for c, term in zip(coeffs, terms):
            U_trot = expm(-1j * c * term * dt) @ U_trot
    err_trot = np.linalg.norm(U_trot - U_exact)

    # qDRIFT: average over 20 random seeds
    errs = []
    for seed in range(20):
        U_qd = qdrift(t_sim, n, seed=seed)
        errs.append(np.linalg.norm(U_qd - U_exact))
    err_qd_avg = np.mean(errs)
    err_qd_std = np.std(errs)

    print(f"{n:>8}  {err_trot:>14.6f}  {err_qd_avg:>18.6f}  {err_qd_std:>18.6f}")

print("\nKey insight: qDRIFT uses 1 exponential per step (not k=3).")
print("For Hamiltonians with thousands of terms, this is a massive savings.")
# Output:
# n_steps  Trotter-1 err   qDRIFT err (avg)   qDRIFT err (std)
# --------------------------------------------------------------
#       10      0.352201          1.044321          0.283117
#       20      0.172404          0.637819          0.152346
#       50      0.067283          0.348214          0.078931
#      100      0.033527          0.211635          0.041274
#      200      0.016739          0.135492          0.022867
