"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.6 The Unitary Constraint: What Makes a Valid Gate
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_11_the_unitary_constraint_what_makes_a_vali.py
"""

import numpy as np

# Quick function to check if a matrix is a valid quantum gate
def is_valid_gate(matrix, label=""):
    """Check if a matrix is unitary (valid quantum gate)."""
    n = matrix.shape[0]
    identity = np.eye(n, dtype=complex)
    is_unit = np.allclose(matrix @ matrix.conj().T, identity)
    print(f"  {label:20s} {'VALID' if is_unit else 'INVALID'} quantum gate")
    return is_unit

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)

# These are valid gates
is_valid_gate(H, "Hadamard")
is_valid_gate(X, "Pauli-X")
is_valid_gate(H @ X @ H, "HXH")

# These are NOT valid gates
bad_gate1 = np.array([[1, 1], [0, 1]], dtype=complex)  # Not unitary
is_valid_gate(bad_gate1, "[[1,1],[0,1]]")

bad_gate2 = np.array([[1, 0], [0, 0.5]], dtype=complex)  # Shrinks probabilities
is_valid_gate(bad_gate2, "[[1,0],[0,0.5]]")

# Classical AND gate -- not reversible, not unitary, not quantum
# AND: (0,0)→0, (0,1)→0, (1,0)→0, (1,1)→1
# Two inputs, one output: information lost! Can't be a quantum gate.
print(f"\n  Classical AND: NOT a valid quantum gate (irreversible)")
