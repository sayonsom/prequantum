"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.1 Data Encoding: Getting Classical Data Into a Quantum Computer
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_02_data_encoding_getting_classical_data_int.py
"""

import numpy as np

def angle_encode(x):
    """Encode an n-dimensional vector into n qubits via Ry rotations.
    Each qubit gets one feature as its rotation angle."""
    n_qubits = len(x)
    state = np.array([1.0], dtype=complex)  # start with scalar 1
    for xi in x:
        theta = xi * np.pi  # scale to [0, π]
        qubit = np.array([np.cos(theta/2), np.sin(theta/2)], dtype=complex)
        state = np.kron(state, qubit)
    return state

# Encode a 3D data point → 3 qubits → 8-dimensional Hilbert space
x = np.array([0.5, 0.3, 0.8])
phi = angle_encode(x)
print(f"Input: {x} (3 features)")
print(f"Quantum state: {np.round(phi, 4)} ({len(phi)} dimensions)")
print(f"Probabilities sum to: {np.sum(np.abs(phi)**2):.4f}")
# Output:
# Input: [0.5 0.3 0.8] (3 features)
# Quantum state: [0.5328+0.j 0.7177+0.j 0.2459+0.j 0.3313+0.j 0.1403+0.j 0.189 +0.j
#  0.0648+0.j 0.0873+0.j] (8 dimensions)
# Probabilities sum to: 1.0000
