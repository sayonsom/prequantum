"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.5 Dequantization: When Classical Algorithms Catch Up
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_11_dequantization_when_classical_algorithms.py
"""

import numpy as np

# The quantum kernel that's hard to dequantize: IQP-like circuits
def iqp_inspired_feature_map(x, n_qubits=4):
    """Feature map inspired by IQP circuits -- believed to be hard
    to simulate classically due to the diagonal ZZ entangling structure.

    The key: all gates commute (they're diagonal in the Z basis),
    but the resulting kernel involves sums of exponentials that
    are #P-hard to compute exactly."""
    dim = 2**n_qubits
    state = np.ones(dim, dtype=complex) / np.sqrt(dim)  # |+...+⟩ (Hadamard all)

    # Diagonal phase gates: Z rotations encoding data
    phases = np.zeros(dim)
    for i in range(dim):
        bitstring = format(i, f'0{n_qubits}b')
        # Single-qubit phases
        for q in range(min(len(x), n_qubits)):
            if bitstring[q] == '1':
                phases[i] += x[q] * np.pi
        # Two-qubit ZZ interaction phases (the hard part)
        for q1 in range(min(len(x), n_qubits)):
            for q2 in range(q1 + 1, min(len(x), n_qubits)):
                if bitstring[q1] == '1' and bitstring[q2] == '1':
                    phases[i] += x[q1] * x[q2] * np.pi

    state = state * np.exp(1j * phases)
    return state

# This kernel is believed to be hard to compute classically
# because evaluating the kernel at a single point requires summing
# 2^n terms with no known shortcut
x1 = np.array([0.3, 0.7, 0.5, 0.2])
x2 = np.array([0.8, 0.1, 0.6, 0.4])
phi1 = iqp_inspired_feature_map(x1)
phi2 = iqp_inspired_feature_map(x2)
k_iqp = np.abs(np.dot(phi1.conj(), phi2))**2
print(f"IQP-inspired kernel value: {k_iqp:.6f}")
print(f"This kernel involves a sum of {2**4} = 16 terms")
print(f"For n qubits, evaluating it classically takes O(2^n) time")
print(f"→ This is where quantum advantage might live")
# Output:
# IQP-inspired kernel value: 0.087792
# This kernel involves a sum of 16 = 16 terms
# For n qubits, evaluating it classically takes O(2^n) time
# → This is where quantum advantage might live
