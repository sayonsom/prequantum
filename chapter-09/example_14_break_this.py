"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_14_break_this.py
"""

import numpy as np

def is_valid_gate(matrix):
    """Check if a matrix is a valid quantum gate (unitary)."""
    n = matrix.shape[0]
    product = matrix.T @ matrix  # BUG: should be .conj().T, not just .T
    return np.allclose(product, np.eye(n))

# Test cases
X = np.array([[0, 1], [1, 0]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
bad = np.array([[1, 1], [0, 1]], dtype=complex)

print(f"X is valid gate? {is_valid_gate(X)}")    # Should be True ✓
print(f"S is valid gate? {is_valid_gate(S)}")    # Should be True -- but says False!
print(f"Y is valid gate? {is_valid_gate(Y)}")    # Should be True -- but says False!
print(f"bad is valid gate? {is_valid_gate(bad)}")  # Should be False ✓
