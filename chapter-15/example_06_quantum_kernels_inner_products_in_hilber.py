"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.2 Quantum Kernels: Inner Products in Hilbert Space
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_06_quantum_kernels_inner_products_in_hilber.py
"""

import numpy as np

def kernel_target_alignment(K, y):
    """Compute kernel-target alignment (KTA).
    KTA ∈ [-1, 1]; higher means the kernel better matches the label structure.
    Cristianini et al. (2001), adapted for quantum kernels by Hubregtsen et al. (2022)."""
    n = len(y)
    # Ideal kernel: K*(i,j) = 1 if y_i == y_j, else -1
    y_signed = 2 * y - 1  # convert {0,1} → {-1,+1}
    K_ideal = np.outer(y_signed, y_signed)

    # Alignment = ⟨K, K*⟩_F / (||K||_F ||K*||_F)
    alignment = np.sum(K * K_ideal) / (
        np.sqrt(np.sum(K * K)) * np.sqrt(np.sum(K_ideal * K_ideal))
    )
    return alignment

# Compare alignments
K_simple = kernel_matrix(X_data, lambda x: quantum_feature_map(x))  # from Beat 2
K_entangling = K_ent  # from above

kta_simple = kernel_target_alignment(K_simple, y_data)
kta_entangling = kernel_target_alignment(K_entangling, y_data)

print(f"Simple angle encoding KTA:     {kta_simple:.4f}")
print(f"Entangling + product KTA:      {kta_entangling:.4f}")
print(f"\nHigher KTA → better kernel for this task")
# Output:
# Simple angle encoding KTA:     0.0213
# Entangling + product KTA:      0.4816
#
# Higher KTA → better kernel for this task
