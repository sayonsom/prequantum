"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_15_break_this.py
"""

import numpy as np
from scipy.linalg import expm

X = np.array([[0, 1], [1, 0]], dtype=complex)
state = np.array([1, 0], dtype=complex)

# Evolve for t = π/2 -- should give |+⟩
t = np.pi / 2
U = expm(-1j * X * t)
evolved = U @ state

# Check if we got |+⟩
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
print(f"Evolved state: {np.round(evolved, 4)}")
print(f"|+⟩ state:     {np.round(plus, 4)}")
print(f"Are they equal? {np.allclose(evolved, plus)}")  # Expect True, gets False!
