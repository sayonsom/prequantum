"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.3 The Geometry: Why It's a Rotation
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_05_the_geometry_why_its_a_rotation.py
"""

import numpy as np

N = 64  # 6 qubits
n = 6
target_idx = 42

# Build the 2D subspace explicitly
w = np.zeros(N, dtype=complex)
w[target_idx] = 1.0
s = np.ones(N, dtype=complex) / np.sqrt(N)

# |s'⟩: component of |s⟩ perpendicular to |w⟩
inner = np.vdot(w, s)  # ⟨w|s⟩ = 1/√N
s_perp = s - inner * w
s_perp = s_perp / np.linalg.norm(s_perp)

# Verify |s⟩ decomposition
theta = np.arcsin(abs(inner))
print(f"θ = arcsin(1/√{N}) = {theta:.6f} rad = {np.degrees(theta):.2f}°")
print(f"1/√N = {1/np.sqrt(N):.6f}")
print(f"sin(θ) = {np.sin(theta):.6f}  (should match 1/√N)")

# Build Grover iterate
I_mat = np.eye(N, dtype=complex)
oracle = I_mat - 2 * np.outer(w, w.conj())
diffusion = 2 * np.outer(s, s.conj()) - I_mat
G = diffusion @ oracle

# Track trajectory in the |w⟩-|s'⟩ plane
state = s.copy()
optimal_k = int(np.round(np.pi / (4 * theta) - 0.5))  # k where (2k+1)θ ≈ π/2
print(f"\nOptimal iterations: {optimal_k}")
print(f"π/(4θ) - 1/2 = {np.pi/(4*theta) - 0.5:.2f}")

print(f"\n{'k':>3}  {'comp_w':>8}  {'comp_s':>8}  {'P(w) actual':>12}  {'P(w) theory':>12}  {'angle':>8}")
for k in range(optimal_k + 3):
    comp_w = np.vdot(w, state).real      # component along |w⟩
    comp_s = np.vdot(s_perp, state).real  # component along |s'⟩
    p_actual = abs(np.vdot(w, state))**2
    angle_theory = (2*k + 1) * theta
    p_theory = np.sin(angle_theory)**2
    print(f"  {k:3d}  {comp_w:+.5f}  {comp_s:+.5f}  {p_actual:11.6f}  {p_theory:11.6f}  {np.degrees(angle_theory):7.1f}°")
    state = G @ state

print(f"\nProbability peaks at k={optimal_k}, then DECREASES.")
print(f"The state has rotated past |w⟩ and is heading back toward |s'⟩.")
