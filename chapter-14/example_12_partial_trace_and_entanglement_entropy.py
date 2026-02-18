"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.5 Partial Trace and Entanglement Entropy
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_12_partial_trace_and_entanglement_entropy.py
"""

import numpy as np

def schmidt_decomposition(psi_AB, dim_A, dim_B):
    """Compute Schmidt decomposition of a bipartite pure state."""
    # Reshape state vector into a dim_A x dim_B matrix
    psi_matrix = psi_AB.reshape(dim_A, dim_B)
    # SVD gives the Schmidt decomposition directly
    U, singular_values, Vh = np.linalg.svd(psi_matrix, full_matrices=False)
    schmidt_coeffs = singular_values**2  # probabilities
    return singular_values, schmidt_coeffs, U, Vh

def entanglement_entropy(schmidt_coeffs):
    """Compute entanglement entropy from Schmidt coefficients."""
    coeffs = schmidt_coeffs[schmidt_coeffs > 1e-12]
    return -np.sum(coeffs * np.log2(coeffs))

# Test on different 2-qubit states
states = {
    "|00⟩ (product)":   np.array([1, 0, 0, 0], dtype=complex),
    "|Φ+⟩ (max ent.)":  np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2),
    "|Ψ−⟩ (max ent.)":  np.array([0, 1, -1, 0], dtype=complex) / np.sqrt(2),
    "Partial ent.":     np.array([np.sqrt(0.8), 0, 0, np.sqrt(0.2)], dtype=complex),
}

print(f"{'State':<20} {'Schmidt coeffs':>20} {'Rank':>5} {'E (bits)':>9}")
print("-" * 58)
for name, psi in states.items():
    sv, sc, _, _ = schmidt_decomposition(psi, 2, 2)
    rank = np.sum(sv > 1e-10)
    E = entanglement_entropy(sc)
    sc_str = ", ".join(f"{c:.3f}" for c in sc if c > 1e-10)
    print(f"{name:<20} {sc_str:>20} {rank:>5} {E:>9.4f}")
# Output:
# State                    Schmidt coeffs  Rank  E (bits)
# ----------------------------------------------------------
# |00⟩ (product)                    1.000     1    0.0000
# |Φ+⟩ (max ent.)            0.500, 0.500     2    1.0000
# |Ψ−⟩ (max ent.)            0.500, 0.500     2    1.0000
# Partial ent.               0.800, 0.200     2    0.7219
