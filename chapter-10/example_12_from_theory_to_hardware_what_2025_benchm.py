"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.9 From Theory to Hardware: What 2025 Benchmarks Reveal
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_12_from_theory_to_hardware_what_2025_benchm.py
"""

import numpy as np

# Simulating the pattern-density effect on BV success rates
# Based on 2025 benchmarking data from 127-qubit processors

def simulate_noisy_bv(secret, error_rate_per_cnot=0.01, shots=1000):
    """Simple noise model: each CNOT has independent bit-flip error."""
    n = len(secret)
    n_cnots = secret.count('1')
    # Probability of getting the right answer ≈ (1 - error)^(2*n_cnots)
    # Factor of 2: each CNOT contributes to 2 qubit errors approximately
    p_success = (1 - error_rate_per_cnot) ** (2 * n_cnots)

    successes = np.random.binomial(shots, p_success)
    return successes / shots

# Compare sparse vs dense secrets for n=8
np.random.seed(42)
secrets = [
    ("10000000", "sparse (1 one)"),
    ("10100000", "medium (2 ones)"),
    ("10101010", "alternating (4 ones)"),
    ("11110000", "half-dense (4 ones)"),
    ("11111110", "dense (7 ones)"),
    ("11111111", "full (8 ones)"),
]

print(f"{'Secret':<12} {'Density':<22} {'Simulated success':>18}")
print("-" * 55)
for secret, desc in secrets:
    rate = simulate_noisy_bv(secret, error_rate_per_cnot=0.015)
    print(f"{secret:<12} {desc:<22} {rate:>17.1%}")

print(f"\nNote: Real hardware results (2025) are much worse than this")
print(f"simple model predicts, due to correlated errors, crosstalk,")
print(f"and structure-dependent noise mechanisms.")
