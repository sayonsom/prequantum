"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.5 Dequantization: When Classical Algorithms Catch Up
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_10_dequantization_when_classical_algorithms.py
"""

import numpy as np

def classical_rff_kernel(X, n_features=100, sigma=1.0, seed=42):
    """Approximate a kernel using Random Fourier Features.
    Rahimi & Recht (2007) -- the classical technique that dequantizes
    many quantum kernel models."""
    rng = np.random.RandomState(seed)
    d = X.shape[1]  # input dimension

    # Sample frequencies from the Fourier transform of the target kernel
    # For RBF kernel: ω ~ N(0, 1/σ²)
    omega = rng.randn(n_features, d) / sigma
    b = rng.uniform(0, 2 * np.pi, n_features)

    # Random feature map: z(x) = sqrt(2/D) * cos(ωx + b)
    Z = np.sqrt(2 / n_features) * np.cos(X @ omega.T + b)

    # Approximate kernel matrix: K ≈ Z @ Z.T
    return Z @ Z.T

# Compare: exact RBF kernel vs RFF approximation
X_data = np.array([
    [0.1, 0.1], [0.2, 0.2], [0.9, 0.9], [0.8, 0.8],
    [0.1, 0.9], [0.2, 0.8], [0.9, 0.1], [0.8, 0.2],
])

def exact_rbf_kernel_matrix(X, sigma=1.0):
    n = len(X)
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K[i, j] = np.exp(-np.linalg.norm(X[i] - X[j])**2 / (2 * sigma**2))
    return K

K_exact = exact_rbf_kernel_matrix(X_data)
K_rff_50 = classical_rff_kernel(X_data, n_features=50)
K_rff_500 = classical_rff_kernel(X_data, n_features=500)

err_50 = np.max(np.abs(K_exact - K_rff_50))
err_500 = np.max(np.abs(K_exact - K_rff_500))

print(f"RFF with D=50  features: max error = {err_50:.4f}")
print(f"RFF with D=500 features: max error = {err_500:.4f}")
print(f"\nWith O(1/ε²) features, RFF approximates the kernel to ε accuracy.")
print(f"If the quantum kernel's Fourier spectrum is efficiently sampleable,")
print(f"then classical RFF achieves the same kernel → no quantum advantage.")
# Output:
# RFF with D=50  features: max error = 0.1342
# RFF with D=500 features: max error = 0.0387
#
# With O(1/ε²) features, RFF approximates the kernel to ε accuracy.
# If the quantum kernel's Fourier spectrum is efficiently sampleable,
# then classical RFF achieves the same kernel → no quantum advantage.
