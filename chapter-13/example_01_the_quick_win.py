"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_01_the_quick_win.py
"""

import numpy as np
from scipy.optimize import minimize

# Hamiltonian: H = -Z⊗Z - 0.5(X⊗I + I⊗X)
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H = -np.kron(Z, Z) - 0.5 * (np.kron(X, I) + np.kron(I, X))

# Exact answer: minimum eigenvalue
eigenvalues = np.linalg.eigvalsh(H)
print(f"Exact eigenvalues: {np.round(eigenvalues, 4)}")
print(f"Ground state energy (exact): {eigenvalues[0]:.6f}")

# VQE: parameterized circuit as a function
def ansatz(params):
    """Build a 2-qubit state from 6 parameters (2 layers)."""
    theta1, theta2, theta3, theta4, theta5, theta6 = params
    # Start with |00⟩
    state = np.array([1, 0, 0, 0], dtype=complex)

    # Layer 1: Ry rotations on each qubit
    Ry1 = np.array([[np.cos(theta1/2), -np.sin(theta1/2)],
                     [np.sin(theta1/2),  np.cos(theta1/2)]], dtype=complex)
    Ry2 = np.array([[np.cos(theta2/2), -np.sin(theta2/2)],
                     [np.sin(theta2/2),  np.cos(theta2/2)]], dtype=complex)
    state = np.kron(Ry1, Ry2) @ state

    # Entangling layer: CNOT
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
    state = CNOT @ state

    # Layer 2: more Ry rotations
    Ry3 = np.array([[np.cos(theta3/2), -np.sin(theta3/2)],
                     [np.sin(theta3/2),  np.cos(theta3/2)]], dtype=complex)
    Ry4 = np.array([[np.cos(theta4/2), -np.sin(theta4/2)],
                     [np.sin(theta4/2),  np.cos(theta4/2)]], dtype=complex)
    state = np.kron(Ry3, Ry4) @ state

    # Second entangling layer
    state = CNOT @ state

    # Layer 3: final rotations
    Ry5 = np.array([[np.cos(theta5/2), -np.sin(theta5/2)],
                     [np.sin(theta5/2),  np.cos(theta5/2)]], dtype=complex)
    Ry6 = np.array([[np.cos(theta6/2), -np.sin(theta6/2)],
                     [np.sin(theta6/2),  np.cos(theta6/2)]], dtype=complex)
    state = np.kron(Ry5, Ry6) @ state

    return state

def cost(params):
    """Compute ⟨ψ(θ)|H|ψ(θ)⟩."""
    state = ansatz(params)
    return np.real(state.conj() @ H @ state)

# Optimize
result = minimize(cost, x0=np.random.randn(6) * 0.1, method='COBYLA',
                  options={'maxiter': 500})

print(f"\nVQE result:              {result.fun:.6f}")
print(f"Error:                   {abs(result.fun - eigenvalues[0]):.8f}")
print(f"Optimal parameters:      {np.round(result.x, 4)}")
