"""Estimate a fidelity kernel with finite shots and inspect PSD repair."""

import numpy as np


def product_angle_kernel(data):
    differences = data[:, None, :] - data[None, :, :]
    return np.prod(np.cos(np.pi * differences / 2) ** 2, axis=2)


def estimate_symmetric_kernel(exact_kernel, shots, seed):
    rng = np.random.default_rng(seed)
    size = exact_kernel.shape[0]
    estimate = np.eye(size)
    for row in range(size):
        for column in range(row + 1, size):
            successes = rng.binomial(shots, exact_kernel[row, column])
            value = successes / shots
            estimate[row, column] = value
            estimate[column, row] = value
    return estimate


def project_to_unit_diagonal_psd(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh((matrix + matrix.T) / 2)
    clipped = np.maximum(eigenvalues, 0.0)
    projected = (eigenvectors * clipped) @ eigenvectors.T
    scales = np.sqrt(np.diag(projected))
    projected = projected / np.outer(scales, scales)
    return (projected + projected.T) / 2


data = np.array([
    [0.10, 0.10], [0.20, 0.20], [0.80, 0.80], [0.90, 0.90],
    [0.10, 0.90], [0.20, 0.80], [0.80, 0.20], [0.90, 0.10],
])
shots = 128
exact = product_angle_kernel(data)
estimated = estimate_symmetric_kernel(exact, shots=shots, seed=0)
repaired = project_to_unit_diagonal_psd(estimated)

estimated_minimum = float(np.min(np.linalg.eigvalsh(estimated)))
repaired_minimum = float(np.min(np.linalg.eigvalsh(repaired)))
estimated_rmse = float(np.sqrt(np.mean((estimated - exact) ** 2)))
repaired_rmse = float(np.sqrt(np.mean((repaired - exact) ** 2)))

assert estimated_minimum < 0.0
assert repaired_minimum >= -1e-12
assert np.allclose(np.diag(repaired), 1.0, atol=1e-12)

print(f"shots_per_pair={shots}")
print(f"estimated_minimum_eigenvalue={estimated_minimum:.6f}")
print(f"repaired_minimum_eigenvalue={repaired_minimum:.3e}")
print(f"estimated_rmse_against_exact={estimated_rmse:.6f}")
print(f"repaired_rmse_against_exact={repaired_rmse:.6f}")
print("boundary=PSD repair changes the matrix; it does not prove accurate hardware estimation")
