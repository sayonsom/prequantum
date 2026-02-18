"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.4 The Stabilizer Formalism: A Unified Language
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_05_the_stabilizer_formalism_a_unified_langu.py
"""

import numpy as np
from functools import reduce

# Pauli matrices
I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.array([[1, 0], [0, -1]])

def kron_list(matrices):
    """Tensor product of a list of matrices."""
    return reduce(np.kron, matrices)

# Stabilizer generators for 3-qubit bit-flip code
S1 = kron_list([Z, Z, I])  # Z₀Z₁: parity of qubits 0,1
S2 = kron_list([I, Z, Z])  # Z₁Z₂: parity of qubits 1,2

# The encoded |0⟩_L = |000⟩
state_0L = np.zeros(8)
state_0L[0b000] = 1.0

# The encoded |1⟩_L = |111⟩
state_1L = np.zeros(8)
state_1L[0b111] = 1.0

# Superposition: |+⟩_L = (|000⟩ + |111⟩)/√2
state_plus_L = (state_0L + state_1L) / np.sqrt(2)

# Verify: stabilizers give +1 on encoded states
print("=== Stabilizer eigenvalues on VALID states ===")
for name, state in [("0_L", state_0L), ("1_L", state_1L), ("+_L", state_plus_L)]:
    ev1 = state @ S1 @ state  # expectation value
    ev2 = state @ S2 @ state
    print(f"  |{name}⟩: S1={ev1:+.0f}, S2={ev2:+.0f}")

# Now introduce an error: X on qubit 1
X1 = kron_list([I, X, I])  # bit flip on qubit 1
error_state = X1 @ state_plus_L

print("\n=== After X error on qubit 1 ===")
ev1 = error_state @ S1 @ error_state
ev2 = error_state @ S2 @ error_state
print(f"  Syndrome: S1={ev1:+.0f}, S2={ev2:+.0f}")
print(f"  Syndrome bits: ({int((1-ev1)/2)}, {int((1-ev2)/2)})")
print(f"  Decode: syndrome (1,1) → error on qubit 1")

# Try X error on qubit 0
error_state_0 = kron_list([X, I, I]) @ state_plus_L
ev1 = error_state_0 @ S1 @ error_state_0
ev2 = error_state_0 @ S2 @ error_state_0
print(f"\n=== After X error on qubit 0 ===")
print(f"  Syndrome: S1={ev1:+.0f}, S2={ev2:+.0f}")
print(f"  Syndrome bits: ({int((1-ev1)/2)}, {int((1-ev2)/2)})")
print(f"  Decode: syndrome (1,0) → error on qubit 0")

# Output:
# === Stabilizer eigenvalues on VALID states ===
#   |0_L⟩: S1=+1, S2=+1
#   |1_L⟩: S1=+1, S2=+1
#   |+_L⟩: S1=+1, S2=+1
#
# === After X error on qubit 1 ===
#   Syndrome: S1=-1, S2=-1
#   Syndrome bits: (1, 1)
#   Decode: syndrome (1,1) → error on qubit 1
#
# === After X error on qubit 0 ===
#   Syndrome: S1=-1, S2=+1
#   Syndrome bits: (1, 0)
#   Decode: syndrome (1,0) → error on qubit 0
