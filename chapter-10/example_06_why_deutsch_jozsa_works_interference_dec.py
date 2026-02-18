"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.4 Why Deutsch-Jozsa Works: Interference Decoded
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_06_why_deutsch_jozsa_works_interference_dec.py
"""

import numpy as np

# Full amplitude analysis: where does probability go for balanced functions?
n = 3
N = 2**n

# Build H⊗n
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
H_n = H
for _ in range(n - 1):
    H_n = np.kron(H_n, H)

# Balanced: f(x) = x₀ (least significant bit)
state_balanced = np.array([(-1)**(x & 1) for x in range(N)]) / np.sqrt(N)
result = H_n @ state_balanced

print("After final Hadamard for f(x) = x₀:")
for i in range(N):
    bits = format(i, f'0{n}b')
    amp = result[i]
    prob = abs(amp)**2
    if prob > 0.001:
        print(f"  |{bits}⟩: amplitude = {amp:.4f}, probability = {prob:.4f}")

# Balanced: f(x) = x₀ ⊕ x₁
state_balanced2 = np.array([(-1)**( (x & 1) ^ ((x >> 1) & 1) ) for x in range(N)]) / np.sqrt(N)
result2 = H_n @ state_balanced2

print("\nAfter final Hadamard for f(x) = x₀ ⊕ x₁:")
for i in range(N):
    bits = format(i, f'0{n}b')
    amp = result2[i]
    prob = abs(amp)**2
    if prob > 0.001:
        print(f"  |{bits}⟩: amplitude = {amp:.4f}, probability = {prob:.4f}")
