"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_14_break_this.py
"""

import numpy as np
from collections import Counter

class BuggyQubit:
    def __init__(self, state=None):
        if state is None:
            state = np.array([1, 0], dtype=complex)
        self.state = np.array(state, dtype=complex)
        # Normalize
        norm = np.sum(np.abs(self.state)**2)  # BUG IS HERE
        self.state = self.state / norm

    def measure(self, rng=None):
        if rng is None:
            rng = np.random.default_rng()
        prob_0 = abs(self.state[0])**2
        result = rng.choice([0, 1], p=[prob_0, 1 - prob_0])
        return result

# State [3, 4] normalized correctly gives [0.6, 0.8]
# So P(0) = 0.36, P(1) = 0.64
# Expected: ~3600 | ~6400
rng = np.random.default_rng(42)
q = BuggyQubit([3, 4])
results = [q.measure(rng) for _ in range(10000)]
counts = Counter(results)
print(f"0: {counts[0]}  |  1: {counts[1]}")
# Actual output is very different from 3600/6400 -- why?
