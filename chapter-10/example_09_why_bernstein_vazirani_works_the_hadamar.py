"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.6 Why Bernstein-Vazirani Works: The Hadamard as Fourier Transform
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_09_why_bernstein_vazirani_works_the_hadamar.py
"""

import numpy as np

# Verify: H⊗n transforms the phase-encoded state into |s⟩
n = 3
N = 2**n
secret = [1, 0, 1]  # s = "101"

# Build the state after oracle: (1/√N) Σ_x (-1)^(s·x) |x⟩
state = np.zeros(N, dtype=complex)
for x in range(N):
    # Compute s · x (bitwise dot product mod 2)
    s_dot_x = 0
    for i in range(n):
        s_dot_x ^= (secret[i] & ((x >> i) & 1))
    state[x] = (-1)**s_dot_x / np.sqrt(N)

print(f"State after oracle: {np.round(state, 4)}")

# Build H⊗n
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
H_n = H
for _ in range(n - 1):
    H_n = np.kron(H_n, H)

# Apply H⊗n
result = H_n @ state
print(f"After H⊗n:         {np.round(result, 4)}")

# Find which basis state has amplitude 1
idx = np.argmax(np.abs(result))
found_bits = format(idx, f'0{n}b')
print(f"Peak at index {idx} = |{found_bits}⟩")
print(f"Secret was: {''.join(str(b) for b in secret)}")
