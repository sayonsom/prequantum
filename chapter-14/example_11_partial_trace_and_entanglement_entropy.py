"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.5 Partial Trace and Entanglement Entropy
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_11_partial_trace_and_entanglement_entropy.py
"""

import numpy as np

def partial_trace_B(rho_AB, dim_A=2, dim_B=2):
    """Trace out subsystem B, returning the reduced density matrix of A."""
    # Reshape into a 4-index tensor: rho[i,j,k,l] where
    # i,k index system A and j,l index system B
    rho_tensor = rho_AB.reshape(dim_A, dim_B, dim_A, dim_B)
    # Trace over B indices (j == l): sum over axis 1 and 3
    rho_A = np.trace(rho_tensor, axis1=1, axis2=3)
    return rho_A

def partial_trace_A(rho_AB, dim_A=2, dim_B=2):
    """Trace out subsystem A, returning the reduced density matrix of B."""
    rho_tensor = rho_AB.reshape(dim_A, dim_B, dim_A, dim_B)
    rho_B = np.trace(rho_tensor, axis1=0, axis2=2)
    return rho_B

# Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
rho_AB = np.outer(bell, bell.conj())

print("Full 2-qubit density matrix (4x4):")
print(np.round(rho_AB, 4))

# Trace out qubit B → get qubit A's state
rho_A = partial_trace_B(rho_AB)
print("\nReduced density matrix of qubit A (2x2):")
print(np.round(rho_A, 4))
print(f"Tr(ρ_A) = {np.trace(rho_A).real:.4f}")
print(f"Tr(ρ_A²) = {np.trace(rho_A @ rho_A).real:.4f}")
print(f"Pure? {np.isclose(np.trace(rho_A @ rho_A), 1.0)}")
# Output:
# Full 2-qubit density matrix (4x4):
# [[0.5+0.j 0. +0.j 0. +0.j 0.5+0.j]
#  [0. +0.j 0. +0.j 0. +0.j 0. +0.j]
#  [0. +0.j 0. +0.j 0. +0.j 0. +0.j]
#  [0.5+0.j 0. +0.j 0. +0.j 0.5+0.j]]
#
# Reduced density matrix of qubit A (2x2):
# [[0.5+0.j 0. +0.j]
#  [0. +0.j 0.5+0.j]]
# Tr(ρ_A) = 1.0000
# Tr(ρ_A²) = 0.5000
# Pure? False
