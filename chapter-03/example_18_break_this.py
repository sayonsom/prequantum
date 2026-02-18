"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_18_break_this.py
"""

import numpy as np
from collections import Counter

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

state = np.array([1, 0, 0, 0], dtype=complex)

# Apply H to qubit 0 and qubit 1
H_both = np.kron(H, H)  # BUG: should be kron(H, I), not kron(H, H)
state = H_both @ state

# Apply CNOT
state = CNOT @ state

# Measure
rng = np.random.default_rng(42)
probs = np.abs(state)**2
outcomes = rng.choice(4, size=10000, p=probs)
labels = {0: "00", 1: "01", 2: "10", 3: "11"}
results = Counter(labels[o] for o in outcomes)

print("Results:")
for label in sorted(results):
    print(f"  {label}: {results[label]}")
# This prints all four outcomes! Not a Bell state.
# The bug: we applied H to BOTH qubits instead of just qubit 0.
