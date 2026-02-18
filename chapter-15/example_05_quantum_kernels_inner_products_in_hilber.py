"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.2 Quantum Kernels: Inner Products in Hilbert Space
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_05_quantum_kernels_inner_products_in_hilber.py
"""

import numpy as np

# A more expressive feature map with entanglement (data re-uploading)
def entangling_feature_map(x, n_layers=2):
    """2-qubit feature map with CNOT entanglement and data re-uploading.
    Multiple layers of encode → entangle create feature interactions."""
    def Ry(t):
        return np.array([[np.cos(t/2), -np.sin(t/2)],
                         [np.sin(t/2),  np.cos(t/2)]], dtype=complex)
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

    state = np.array([1, 0, 0, 0], dtype=complex)  # |00⟩
    for _ in range(n_layers):
        # Data encoding layer
        state = np.kron(Ry(x[0]*np.pi), Ry(x[1]*np.pi)) @ state
        # Entanglement layer
        state = CNOT @ state
        # Cross-feature encoding: encode x[0]*x[1] as additional rotation
        state = np.kron(Ry(x[0]*x[1]*np.pi), np.eye(2)) @ state
    return state

# Build kernel matrix for XOR-like data
X_data = np.array([
    [0.1, 0.1], [0.2, 0.2], [0.9, 0.9], [0.8, 0.8],  # Class 0 (low-low, high-high)
    [0.1, 0.9], [0.2, 0.8], [0.9, 0.1], [0.8, 0.2],  # Class 1 (low-high, high-low)
])
y_data = np.array([0, 0, 0, 0, 1, 1, 1, 1])

def kernel_matrix(X, feature_map):
    n = len(X)
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            phi_i = feature_map(X[i])
            phi_j = feature_map(X[j])
            K[i, j] = np.abs(np.dot(phi_i.conj(), phi_j))**2
    return K

K_ent = kernel_matrix(X_data, entangling_feature_map)

# Check: do within-class similarities exceed between-class?
class_0_avg = np.mean([K_ent[i, j] for i in range(4) for j in range(4) if i != j])
class_1_avg = np.mean([K_ent[i, j] for i in range(4, 8) for j in range(4, 8) if i != j])
between_avg = np.mean([K_ent[i, j] for i in range(4) for j in range(4, 8)])

print(f"Avg within-class 0 kernel: {class_0_avg:.4f}")
print(f"Avg within-class 1 kernel: {class_1_avg:.4f}")
print(f"Avg between-class kernel:  {between_avg:.4f}")
print(f"\nSeparation ratio: {(class_0_avg + class_1_avg) / 2 / max(between_avg, 1e-10):.2f}x")
# Output:
# Avg within-class 0 kernel: 0.6148
# Avg within-class 1 kernel: 0.6148
# Avg between-class kernel:  0.1532
#
# Separation ratio: 4.01x
