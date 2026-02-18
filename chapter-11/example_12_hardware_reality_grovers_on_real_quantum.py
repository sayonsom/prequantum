"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.9 Hardware Reality: Grover's on Real Quantum Computers (2025-26)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_12_hardware_reality_grovers_on_real_quantum.py
"""

import numpy as np

# Model: Grover success probability under depolarizing noise
# P_success ≈ P_ideal × (1 - ε)^(g × k)
# where ε = error per gate, g = gates per Grover iteration, k = iterations

def noisy_grover_success(n, error_per_gate, gates_per_iter=None):
    """Estimate Grover success probability with gate errors."""
    N = 2**n
    k = int(np.pi/4 * np.sqrt(N))  # optimal iterations
    if gates_per_iter is None:
        gates_per_iter = 6*n + 2  # approximate: oracle + diffusion
    total_gates = gates_per_iter * k
    p_ideal = 1.0  # near-certainty at optimal k
    p_noisy = p_ideal * (1 - error_per_gate)**total_gates
    return p_noisy, k, total_gates

print("Grover success probability under gate noise:")
print(f"{'n':>3}  {'N':>6}  {'iters':>5}  {'gates':>7}  "
      f"{'ε=0.1%':>8}  {'ε=0.01%':>8}  {'ε=0.001%':>8}")

for n in [3, 4, 5, 6, 8, 10, 12, 16, 20]:
    N = 2**n
    results = []
    for eps in [0.001, 0.0001, 0.00001]:
        p, k, g = noisy_grover_success(n, eps)
        results.append(p)
    print(f"  {n:3d}  {N:6d}  {k:5d}  {g:7d}  "
          f"{results[0]:8.4f}  {results[1]:8.4f}  {results[2]:8.4f}")

print("\nKey takeaway: even at 0.01% error rate (state-of-the-art 2025),")
print("Grover's becomes useless beyond ~12 qubits without error correction.")
print("This is the 'double exponential decay' -- the algorithm needs √N iterations,")
print("each with O(n) gates, so total error grows as exp(n × 2^(n/2)).")
