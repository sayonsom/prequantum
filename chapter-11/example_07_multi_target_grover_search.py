"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.5 Multi-Target Grover Search
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_07_multi_target_grover_search.py
"""

import numpy as np

N = 32  # 5 qubits
n = 5
targets = [3, 11, 19, 27]  # M = 4 targets
M = len(targets)

# Build oracle for multiple targets
I_mat = np.eye(N, dtype=complex)
oracle = I_mat.copy()
for t in targets:
    w = np.zeros(N, dtype=complex)
    w[t] = 1.0
    oracle -= 2 * np.outer(w, w.conj())

# Diffusion
s = np.ones(N, dtype=complex) / np.sqrt(N)
diffusion = 2 * np.outer(s, s.conj()) - I_mat
grover = diffusion @ oracle

# Optimal iterations for M targets: π/(4θ) where θ = arcsin(√(M/N))
theta = np.arcsin(np.sqrt(M / N))
optimal_k = int(np.round(np.pi / (4 * theta) - 0.5))
print(f"N={N}, M={M} targets, θ={np.degrees(theta):.1f}°, optimal iterations={optimal_k}")
print(f"Compare single-target: {int(np.round(np.pi * np.sqrt(N) / 4))} iterations\n")

state = s.copy()
for k in range(optimal_k + 3):
    p_targets = sum(abs(state[t])**2 for t in targets)
    bar = '#' * int(p_targets * 50)
    print(f"  k={k}: P(any target) = {p_targets:.4f}  {bar}")
    state = grover @ state

# Key insight: more targets → fewer iterations
print(f"\nWith {M} targets out of {N}: {optimal_k} iterations")
print(f"With 1 target out of {N}: ~{int(np.pi/4 * np.sqrt(N))} iterations")
print(f"Speedup from multiple targets: {np.sqrt(N/M)/np.sqrt(N)*np.sqrt(N):.1f}x fewer iterations")
