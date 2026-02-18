"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_01_the_quick_win.py
"""

import numpy as np
from collections import Counter

# Don't worry about these lines yet -- we'll build each one from scratch
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

state = np.array([1, 0, 0, 0], dtype=complex)   # two qubits, both 0
state = np.kron(H, I) @ state                     # do something to qubit 0
state = CNOT @ state                               # entangle them

rng = np.random.default_rng(42)
probs = np.abs(state)**2
outcomes = rng.choice([0, 1, 2, 3], size=10000, p=probs)
labels = {0: "00", 1: "01", 2: "10", 3: "11"}
results = Counter(labels[o] for o in outcomes)
for label in sorted(results):
    print(f"  {label}: {results[label]}")
# 00: ~5000
# 11: ~5000
