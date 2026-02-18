"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.1 Data Encoding: Getting Classical Data Into a Quantum Computer
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_03_data_encoding_getting_classical_data_int.py
"""

import numpy as np

def amplitude_encode(x):
    """Encode a data vector as quantum amplitudes.
    Input must have length 2^n. Gets normalized automatically."""
    # Pad to nearest power of 2 if needed
    n = len(x)
    n_padded = 2**int(np.ceil(np.log2(max(n, 2))))
    padded = np.zeros(n_padded, dtype=complex)
    padded[:n] = x
    # Normalize to unit length (valid quantum state)
    norm = np.linalg.norm(padded)
    if norm < 1e-10:
        raise ValueError("Cannot encode the zero vector")
    return padded / norm

# Encode 4 features into 2 qubits
x = np.array([1.0, 2.0, 3.0, 4.0])
phi = amplitude_encode(x)
n_qubits = int(np.log2(len(phi)))
print(f"Input: {x} (4 features)")
print(f"Quantum state: {np.round(phi.real, 4)} ({n_qubits} qubits)")
print(f"Probabilities: {np.round(np.abs(phi)**2, 4)}")
print(f"Sum: {np.sum(np.abs(phi)**2):.4f}")
# Output:
# Input: [1. 2. 3. 4.] (4 features)
# Quantum state: [0.1826 0.3651 0.5477 0.7303] (2 qubits)
# Probabilities: [0.0333 0.1333 0.3    0.5333]
# Sum: 1.0000
