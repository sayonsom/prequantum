"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.3 Approximate QFT and Gate Pruning
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_04_approximate_qft_and_gate_pruning.py
"""

import numpy as np

# Demonstrate: phase rotation magnitude drops exponentially with k
print("Controlled-R_k rotation angles:")
print(f"{'k':>3s}  {'angle (rad)':>12s}  {'angle (deg)':>12s}  {'|1 - e^(iθ)|':>14s}")
print("-" * 50)

for k in range(1, 13):
    angle = 2 * np.pi / (2**k)
    error = abs(1 - np.exp(1j * angle))
    print(f"{k:3d}  {angle:12.6f}  {np.degrees(angle):12.4f}  {error:14.2e}")

# For n=20 qubits (factoring ~1M-bit numbers):
# Full QFT: 20*19/2 = 190 controlled-phase gates
# Approximate QFT (keep k ≤ 10): only ~10*20 = 200 gates → O(n log n)
# Error from dropping R_k for k>10: ε ≈ n * 2π/2^11 ≈ 0.06

n = 20
full_gates = n * (n - 1) // 2
for k_max in [5, 8, 10, 15]:
    approx_gates = sum(min(k_max, n - 1 - j) for j in range(n))
    dropped = full_gates - approx_gates
    max_phase_error = n * 2 * np.pi / 2**(k_max + 1)
    print(f"\nn={n}, keep R_k for k≤{k_max}:")
    print(f"  Gates: {approx_gates}/{full_gates} ({dropped} dropped)")
    print(f"  Max accumulated phase error: {max_phase_error:.4f} rad")
    print(f"  Fidelity lower bound: {np.cos(max_phase_error/2)**2:.6f}")
