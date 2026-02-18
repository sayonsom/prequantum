"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.2 The Diffusion Operator: Reflect About the Mean
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_03_the_diffusion_operator_reflect_about_the.py
"""

import numpy as np

N = 8
n = 3

# Uniform superposition
s = np.ones(N, dtype=complex) / np.sqrt(N)

# Diffusion operator: 2|s⟩⟨s| - I
I = np.eye(N, dtype=complex)
diffusion = 2 * np.outer(s, s.conj()) - I

print("Diffusion matrix (rounded):")
print(np.round(diffusion.real, 4))
# Every diagonal entry = 2/N - 1 = 2/8 - 1 = -0.75
# Every off-diagonal entry = 2/N = 2/8 = 0.25

# What does it do? Reflect amplitudes about their mean.
# Before: all amplitudes equal except one is negative (from oracle)
target_idx = 5
state = np.ones(N, dtype=complex) / np.sqrt(N)
state[target_idx] *= -1  # Oracle flipped this phase

print(f"\nBefore diffusion:")
mean_amp = np.mean(state.real)
print(f"  Mean amplitude: {mean_amp:.4f}")
for i in range(N):
    label = f"|{format(i, f'0{n}b')}⟩"
    marker = " ← target (negative)" if i == target_idx else ""
    print(f"  {label}: {state[i].real:+.4f}{marker}")

# Apply diffusion
state = diffusion @ state

print(f"\nAfter diffusion:")
for i in range(N):
    label = f"|{format(i, f'0{n}b')}⟩"
    prob = abs(state[i])**2
    marker = " ← target (boosted!)" if i == target_idx else ""
    print(f"  {label}: amp={state[i].real:+.4f}, prob={prob:.4f}{marker}")
