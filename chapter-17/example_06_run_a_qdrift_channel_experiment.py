"""Estimate qDRIFT channel error with deterministic Monte Carlo trials."""

import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

paulis = [np.kron(Z, Z), np.kron(X, I), np.kron(I, X)]
coefficients = np.array([1.0, 0.7, 0.7])
hamiltonian = sum(c * p for c, p in zip(coefficients, paulis))
lambda_1 = np.abs(coefficients).sum()
time = 0.6
psi_0 = np.array([1, 0, 0, 0], dtype=complex)
rho_exact = np.outer(
    expm(-1j * hamiltonian * time) @ psi_0,
    (expm(-1j * hamiltonian * time) @ psi_0).conj(),
)


def qdrift_average(steps: int, trials: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    probabilities = np.abs(coefficients) / lambda_1
    angle = lambda_1 * time / steps
    step_unitaries = [
        expm(-1j * np.sign(c) * angle * p)
        for c, p in zip(coefficients, paulis)
    ]
    rho_sum = np.zeros((4, 4), dtype=complex)
    for _ in range(trials):
        psi = psi_0.copy()
        for term_index in rng.choice(len(paulis), size=steps, p=probabilities):
            psi = step_unitaries[term_index] @ psi
        rho_sum += np.outer(psi, psi.conj())
    return rho_sum / trials


print("steps   trace distance   qDRIFT bound")
for steps in [20, 50, 100, 200]:
    rho_average = qdrift_average(steps, trials=1_000, seed=1706 + steps)
    singular_values = np.linalg.svd(rho_average - rho_exact, compute_uv=False)
    trace_distance = 0.5 * singular_values.sum()
    bound = min(1.0, 2 * lambda_1**2 * time**2 / steps)
    print(f"{steps:5d}   {trace_distance:14.6f}   {bound:13.6f}")

