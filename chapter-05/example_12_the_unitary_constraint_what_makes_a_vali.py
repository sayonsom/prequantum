"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.6 The Unitary Constraint: What Makes a Valid Gate
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_12_the_unitary_constraint_what_makes_a_vali.py
"""

import numpy as np

# Unitarity preserves probability
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
state = np.array([0.6, 0.8j], dtype=complex)  # |α|²+|β|² = 0.36+0.64 = 1

print(f"Before H: total prob = {np.sum(np.abs(state)**2):.4f}")
after = H @ state
print(f"After H:  total prob = {np.sum(np.abs(after)**2):.4f}")
# Both 1.0000

# Non-unitary matrix BREAKS probability conservation
bad = np.array([[2, 0], [0, 1]], dtype=complex)
broken = bad @ state
print(f"\nAfter bad: total prob = {np.sum(np.abs(broken)**2):.4f}")
# 1.44 + 0.64 = 2.08 -- probabilities > 1! Physically meaningless.
