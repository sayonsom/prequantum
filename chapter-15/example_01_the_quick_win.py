"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_01_the_quick_win.py
"""

import numpy as np
from scipy.optimize import minimize

# Generate a simple 2-class dataset (XOR-like, not linearly separable)
np.random.seed(42)
X_train = np.array([
    [0.2, 0.3], [0.3, 0.2], [0.8, 0.9], [0.9, 0.8],  # Class 0
    [0.2, 0.8], [0.3, 0.9], [0.8, 0.2], [0.9, 0.3],  # Class 1
])
y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Quantum feature map: encode (x1, x2) into a 2-qubit state
def quantum_feature_map(x):
    """Encode a 2D point into a 4-dimensional quantum state."""
    # Angle encoding: each feature becomes a rotation angle
    theta1, theta2 = x[0] * np.pi, x[1] * np.pi
    # Single-qubit states from Ry rotations
    q1 = np.array([np.cos(theta1/2), np.sin(theta1/2)])
    q2 = np.array([np.cos(theta2/2), np.sin(theta2/2)])
    # 2-qubit state via tensor product
    return np.kron(q1, q2)

# Quantum kernel: K(x, x') = |⟨φ(x)|φ(x')⟩|²
def quantum_kernel(x1, x2):
    phi1 = quantum_feature_map(x1)
    phi2 = quantum_feature_map(x2)
    overlap = np.abs(np.dot(phi1.conj(), phi2))**2
    return overlap

# Build the kernel matrix
n = len(X_train)
K = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        K[i, j] = quantum_kernel(X_train[i], X_train[j])

print("Quantum kernel matrix:")
print(np.round(K, 3))
print(f"\nKernel matrix shape: {K.shape}")
print(f"Diagonal (self-overlap): {np.round(np.diag(K), 3)}")
# Output:
# Quantum kernel matrix:
# [[1.    0.952 0.119 0.103 0.5   0.337 0.337 0.206]
#  [0.952 1.    0.103 0.119 0.337 0.206 0.5   0.337]
#  [0.119 0.103 1.    0.952 0.337 0.5   0.206 0.337]
#  [0.103 0.119 0.952 1.    0.206 0.337 0.337 0.5  ]
#  [0.5   0.337 0.337 0.206 1.    0.952 0.119 0.103]
#  [0.337 0.206 0.5   0.337 0.952 1.    0.103 0.119]
#  [0.337 0.5   0.206 0.337 0.119 0.103 1.    0.952]
#  [0.206 0.337 0.337 0.5   0.103 0.119 0.952 1.   ]]
#
# Kernel matrix shape: (8, 8)
# Diagonal (self-overlap): [1. 1. 1. 1. 1. 1. 1. 1.]
