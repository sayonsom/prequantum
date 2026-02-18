"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.4 Putting It Together: Full Grover's Algorithm
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_06_putting_it_together_full_grovers_algorit.py
"""

import numpy as np

N = 16  # 4 qubits → 16 items
n = 4
target_idx = 11  # searching for |1011⟩

# Build operators
I = np.eye(N, dtype=complex)
w = np.zeros(N, dtype=complex)
w[target_idx] = 1.0
s = np.ones(N, dtype=complex) / np.sqrt(N)

oracle = I - 2 * np.outer(w, w.conj())
diffusion = 2 * np.outer(s, s.conj()) - I
grover = diffusion @ oracle

# Initial state: uniform superposition
state = s.copy()

# Optimal number of iterations: π√N / 4
optimal_iters = int(np.round(np.pi * np.sqrt(N) / 4))
print(f"N = {N}, optimal iterations = {optimal_iters}")
print(f"Target: |{format(target_idx, f'0{n}b')}⟩\n")

# Run and track
for k in range(optimal_iters + 2):  # go a bit past optimal to show overshooting
    target_prob = abs(state[target_idx])**2
    other_prob = sum(abs(state[i])**2 for i in range(N) if i != target_idx)
    bar = '#' * int(target_prob * 50)
    print(f"  Iter {k}: P(target) = {target_prob:.4f}  P(other) = {other_prob:.4f}  {bar}")

    if k < optimal_iters + 1:
        state = grover @ state

print(f"\nNotice: probability peaks at iteration {optimal_iters}, then DECREASES.")
print("Grover's is like a pendulum -- iterate too many times and you overshoot!")
