"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_01_the_quick_win.py
"""

import numpy as np
from collections import Counter

# The T gate: a subtle phase rotation
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

# Apply H, then T, then H to |0⟩
ket_0 = np.array([1, 0], dtype=complex)
state = H @ T @ H @ ket_0

print(f"State after HTH|0⟩: {np.round(state, 4)}")
print(f"P(0) = {abs(state[0])**2:.4f}")
print(f"P(1) = {abs(state[1])**2:.4f}")
# P(0) ≈ 0.8536
# P(1) ≈ 0.1464

# Verify with measurements
rng = np.random.default_rng(42)
probs = np.abs(state)**2
results = rng.choice([0, 1], size=10000, p=probs)
counts = Counter(results)
print(f"\n10,000 shots: 0→{counts[0]}  1→{counts[1]}")
# ~85% zeros, ~15% ones. Not a coin flip anymore.
