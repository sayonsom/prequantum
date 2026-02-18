"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 4: The AI Lab > Break This (Advanced)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_15_break_this_advanced.py
"""

import numpy as np

def is_valid_kernel_matrix(K, tol=0.0):
    """Check if K is a valid kernel matrix (positive semi-definite)."""
    eigenvalues = np.linalg.eigvalsh(K)
    return np.all(eigenvalues >= tol)

# Kernel matrix from a real quantum computer (with shot noise)
K_noisy = np.array([
    [1.000, 0.312, 0.287, 0.098],
    [0.312, 1.000, 0.156, 0.201],
    [0.287, 0.156, 1.000, 0.345],
    [0.098, 0.201, 0.345, 1.000],
])
# Add realistic shot noise
np.random.seed(7)
K_noisy += np.random.randn(4, 4) * 0.01
K_noisy = (K_noisy + K_noisy.T) / 2  # keep symmetric
np.fill_diagonal(K_noisy, 1.0)

print(f"Valid? {is_valid_kernel_matrix(K_noisy)}")
print(f"Min eigenvalue: {min(np.linalg.eigvalsh(K_noisy)):.6f}")
