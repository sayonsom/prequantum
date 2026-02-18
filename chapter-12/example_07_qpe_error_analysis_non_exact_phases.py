"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.5 QPE Error Analysis: Non-Exact Phases
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_07_qpe_error_analysis_non_exact_phases.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# QPE error analysis: probability distribution for non-exact phase

n_count = 5  # counting qubits
N = 2**n_count

# True phase: φ = 1/3 (not exactly representable in binary)
phi = 1/3

def qpe_probability(m, phi, n):
    """Probability of measuring m in n-qubit QPE with true phase phi."""
    N = 2**n
    delta = N * phi - m
    if abs(delta) < 1e-10:
        return 1.0  # exact case
    return (np.sin(np.pi * delta)**2) / (N * np.sin(np.pi * delta / N))**2

# Compute probabilities for all outcomes
probs = [qpe_probability(m, phi, n_count) for m in range(N)]

# Best approximation: round(N*phi) = round(32/3) = 11
best_m = round(N * phi)
measured_phase = best_m / N

print(f"True phase: φ = 1/3 = {phi:.6f}")
print(f"Best n-bit approximation: {best_m}/{N} = {measured_phase:.6f}")
print(f"Error: |φ - m/N| = {abs(phi - measured_phase):.6f}")
print(f"\nProbability distribution (top 8):")

sorted_probs = sorted(enumerate(probs), key=lambda x: -x[1])
total_top2 = 0
for m, p in sorted_probs[:8]:
    marker = " ←" if m == best_m else ""
    print(f"  m={m:2d}  ({m:05b})  φ̂={m/N:.4f}  P={p:.4f}{marker}")
    if abs(m - best_m) <= 1:
        total_top2 += p

print(f"\nP(|m - best| ≤ 1) = {total_top2:.4f}")
print(f"Theoretical bound: 4/π² = {4/np.pi**2:.4f}")

# How success probability scales with extra precision qubits
print(f"\nSuccess probability vs. extra precision qubits:")
for extra in range(6):
    n = 3 + extra  # minimum bits for denominator + extra
    N = 2**n
    best = round(N * phi)
    p_success = sum(qpe_probability(m, phi, n)
                    for m in range(N) if abs(m - best) <= 1)
    print(f"  n={n}: P(success) = {p_success:.4f}")
