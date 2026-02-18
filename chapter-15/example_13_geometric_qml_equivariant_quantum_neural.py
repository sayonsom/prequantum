"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.7 Geometric QML: Equivariant Quantum Neural Networks
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_13_geometric_qml_equivariant_quantum_neural.py
"""

import numpy as np

# Demonstration: permutation-equivariant quantum circuit
# For a 2-qubit system, the permutation group S₂ has one non-trivial element: SWAP
# A permutation-equivariant circuit must commute with SWAP

def swap_gate():
    """SWAP gate: exchanges two qubits."""
    return np.array([[1,0,0,0],
                     [0,0,1,0],
                     [0,1,0,0],
                     [0,0,0,1]], dtype=complex)

def permutation_equivariant_layer(params):
    """A 2-qubit layer that commutes with SWAP.
    Only uses symmetric combinations of single-qubit gates
    plus a symmetric entangling gate.

    This is the quantum analogue of a weight-sharing CNN:
    the same "filter" is applied regardless of qubit ordering."""
    theta_shared, phi_entangle = params

    # Same rotation on both qubits (weight sharing)
    def Ry(t):
        return np.array([[np.cos(t/2), -np.sin(t/2)],
                         [np.sin(t/2),  np.cos(t/2)]], dtype=complex)

    single_qubit_layer = np.kron(Ry(theta_shared), Ry(theta_shared))

    # Symmetric entangling gate: e^{i φ (XX + YY + ZZ)}
    # This is the isotropic Heisenberg interaction -- it commutes with SWAP
    XX = np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]], dtype=complex)
    YY = np.array([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]], dtype=complex)
    ZZ = np.diag([1, -1, -1, 1]).astype(complex)
    H_ent = phi_entangle * (XX + YY + ZZ)
    entangling = np.eye(4, dtype=complex)
    # Matrix exponential via eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(H_ent)
    entangling = eigenvectors @ np.diag(np.exp(-1j * eigenvalues)) @ eigenvectors.conj().T

    return entangling @ single_qubit_layer

# Verify equivariance: U_layer @ SWAP = SWAP @ U_layer
SWAP = swap_gate()
params = np.array([0.7, 0.3])
U = permutation_equivariant_layer(params)

commutator_norm = np.linalg.norm(U @ SWAP - SWAP @ U)
print(f"||[U, SWAP]|| = {commutator_norm:.2e}")
print(f"Equivariant? {'Yes' if commutator_norm < 1e-10 else 'No'}")
print(f"\nParameters per layer: 2 (vs 4+ for unconstrained)")
print(f"Search space is exponentially smaller → no barren plateau")
# Output:
# ||[U, SWAP]|| = 4.16e-17
# Equivariant? Yes
#
# Parameters per layer: 2 (vs 4+ for unconstrained)
# Search space is exponentially smaller → no barren plateau
