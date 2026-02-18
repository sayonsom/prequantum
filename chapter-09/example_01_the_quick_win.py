"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_01_the_quick_win.py
"""

import numpy as np

# The state |+⟩ in the computational basis {|0⟩, |1⟩}
ket_plus_computational = np.array([1, 1], dtype=complex) / np.sqrt(2)
print(f"|+⟩ in computational basis: {np.round(ket_plus_computational, 4)}")

# The Hadamard basis: {|+⟩, |−⟩}
ket_plus_hadamard = np.array([1, 0], dtype=complex)  # It's the "first" basis vector!
print(f"|+⟩ in Hadamard basis:      {ket_plus_hadamard}")

# Same state, different coordinates. Is this really the same state?
# Yes. The Hadamard matrix converts between the two:
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

# Computational → Hadamard
converted = H @ ket_plus_computational
print(f"\nH @ |+⟩_comp = {np.round(converted, 4)}")  # [1, 0] -- matches!

# Hadamard → Computational
back = H @ ket_plus_hadamard
print(f"H @ |+⟩_had  = {np.round(back, 4)}")  # [0.7071, 0.7071] -- matches!

# The Hadamard gate IS a change-of-basis matrix.
# H takes you from computational basis to Hadamard basis (and back, since H = H†).
print(f"\nH @ H = I? {np.allclose(H @ H, np.eye(2))}")  # True
