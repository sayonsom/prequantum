"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_11_break_this.py
"""

import numpy as np
from scipy.optimize import minimize

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H = -np.kron(Z, Z) - 0.5 * (np.kron(X, I) + np.kron(I, X))

def buggy_ansatz(params):
    state = np.array([1, 0, 0, 0], dtype=complex)
    theta1, theta2 = params
    Ry1 = np.array([[np.cos(theta1/2), -np.sin(theta1/2)],
                     [np.sin(theta1/2),  np.cos(theta1/2)]], dtype=complex)
    Ry2 = np.array([[np.cos(theta2/2), -np.sin(theta2/2)],
                     [np.sin(theta2/2),  np.cos(theta2/2)]], dtype=complex)
    state = np.kron(Ry1, Ry2) @ state
    # BUG: no entangling gate! Without CNOT, the ansatz can only produce
    # product states |ψ₁⟩⊗|ψ₂⟩, which can't represent entangled ground states.
    return state

def cost(params):
    state = buggy_ansatz(params)
    return np.real(state.conj() @ H @ state)

result = minimize(cost, x0=[0.1, 0.1], method='COBYLA')

exact_E0 = np.linalg.eigvalsh(H)[0]
print(f"VQE energy:  {result.fun:.6f}")
print(f"Exact E₀:    {exact_E0:.6f}")
print(f"Error:       {abs(result.fun - exact_E0):.6f}")
print(f"VQE is WRONG because ansatz can't represent entangled states!")
