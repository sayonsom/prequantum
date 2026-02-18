"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_01_the_quick_win.py
"""

import numpy as np
from collections import Counter

# A qubit in superposition
state = np.array([1, 1]) / np.sqrt(2)

# Measure it 10,000 times
rng = np.random.default_rng(42)
results = rng.choice([0, 1], size=10000, p=[abs(state[0])**2, abs(state[1])**2])
counts = Counter(results)

print(f"0: {counts[0]} times ({counts[0]/100:.1f}%)")
print(f"1: {counts[1]} times ({counts[1]/100:.1f}%)")
# 0: 4976 times (49.8%)
# 1: 5024 times (50.2%)
