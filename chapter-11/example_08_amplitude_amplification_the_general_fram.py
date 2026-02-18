"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.6 Amplitude Amplification: The General Framework
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_08_amplitude_amplification_the_general_fram.py
"""

import numpy as np

N = 16
n = 4

# Suppose algorithm A prepares a non-uniform state
# (e.g., some quantum heuristic that has ~25% chance of finding the answer)
np.random.seed(42)
A_state = np.random.randn(N) + 1j * np.random.randn(N)
A_state = A_state / np.linalg.norm(A_state)

# Mark items 3 and 7 as "good"
good = {3, 7}
p_good = sum(abs(A_state[i])**2 for i in good)
print(f"Initial success probability: {p_good:.4f}")

# Build A as a unitary (for demonstration, use a random unitary that maps |0⟩ to A_state)
# In practice, A is your quantum algorithm
from scipy.stats import unitary_group
# We need A|0⟩ = A_state. Build A by extending A_state to a full unitary.
A_mat = np.eye(N, dtype=complex)
A_mat[:, 0] = A_state  # first column is our desired state
# Gram-Schmidt to make it unitary
for j in range(1, N):
    for k in range(j):
        A_mat[:, j] -= np.vdot(A_mat[:, k], A_mat[:, j]) * A_mat[:, k]
    norm = np.linalg.norm(A_mat[:, j])
    if norm > 1e-10:
        A_mat[:, j] /= norm

# Operators
I_mat = np.eye(N, dtype=complex)
S_f = I_mat.copy()
for g in good:
    S_f[g, g] = -1  # mark good states

zero = np.zeros(N, dtype=complex)
zero[0] = 1.0
S_0 = I_mat - 2 * np.outer(zero, zero.conj())  # reflect about |0⟩

# Amplitude amplification iterate: A · S_0 · A† · S_f
G_aa = A_mat @ S_0 @ A_mat.conj().T @ S_f

# Run
theta_aa = np.arcsin(np.sqrt(p_good))
optimal_k = int(np.round(np.pi / (4 * theta_aa) - 0.5))
print(f"θ = {np.degrees(theta_aa):.1f}°, optimal iterations = {optimal_k}")

state = A_state.copy()
for k in range(optimal_k + 2):
    p = sum(abs(state[i])**2 for i in good)
    bar = '#' * int(p * 50)
    print(f"  k={k}: P(good) = {p:.4f}  {bar}")
    state = G_aa @ state
