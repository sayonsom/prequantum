"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.4 Why Deutsch-Jozsa Works: Interference Decoded
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_05_why_deutsch_jozsa_works_interference_dec.py
"""

import numpy as np

# Numerical verification of the interference argument
n = 4
N = 2**n  # 16 possible inputs

# Constant function: f(x) = 0 for all x
phases_constant = np.array([(-1)**0 for _ in range(N)])
amplitude_constant = np.sum(phases_constant) / N
print(f"Constant f=0: amplitude of |0000⟩ = {amplitude_constant:.4f}")  # 1.0

# Balanced function: f(x) = x₀ (first bit)
phases_balanced = np.array([(-1)**(x & 1) for x in range(N)])
amplitude_balanced = np.sum(phases_balanced) / N
print(f"Balanced f=x₀: amplitude of |0000⟩ = {amplitude_balanced:.4f}")  # 0.0

# The math: constant → all phases align (constructive interference)
#           balanced → half +1, half -1 (destructive interference)
print(f"\nConstant phases:  {phases_constant[:8]}... (all same)")
print(f"Balanced phases:  {phases_balanced[:8]}... (alternating)")
print(f"Sum constant: {np.sum(phases_constant)}")
print(f"Sum balanced: {np.sum(phases_balanced)}")
