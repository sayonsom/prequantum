"""Separate exact state evolution from finite-shot observation."""

import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H = np.kron(Z, Z) + 0.7 * (np.kron(X, I) + np.kron(I, X))
psi_0 = np.array([1, 0, 0, 0], dtype=complex)
time = 0.8
psi_t = expm(-1j * H * time) @ psi_0
probabilities = np.abs(psi_t) ** 2

# Measurement in the computational basis estimates Z on each qubit.
basis = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
z_values = 1 - 2 * basis
magnetization_per_outcome = z_values.mean(axis=1)
exact_magnetization = probabilities @ magnetization_per_outcome

rng = np.random.default_rng(1705)
shots = 4_000
samples = rng.choice(4, size=shots, p=probabilities)
estimated_magnetization = magnetization_per_outcome[samples].mean()
standard_error = magnetization_per_outcome[samples].std(ddof=1) / np.sqrt(shots)

print("probabilities:", np.round(probabilities, 6))
print(f"exact <M_z>:     {exact_magnetization:.6f}")
print(f"shot estimate:   {estimated_magnetization:.6f}")
print(f"standard error:  {standard_error:.6f}")
print(f"within 3 SE:     {abs(estimated_magnetization-exact_magnetization) <= 3*standard_error}")

