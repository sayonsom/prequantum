"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.6 Error Mitigation: Fighting Noise Without Error Correction
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_11_error_mitigation_fighting_noise_without.py
"""

import numpy as np

# Conceptual demo of PEC (simplified)
# If the noisy CNOT is: ρ → (1-p) * CNOT(ρ) + p * depolarized(ρ)
# Then ideal CNOT = noisy_CNOT / (1-p) - (p/(1-p)) * depolarized
# The "cost" is 1/(1-p)^n for n gates -- exponential in circuit depth

p = 0.01  # 1% depolarizing error per CX gate

for n_gates in [1, 5, 10, 20, 50, 100]:
    # PEC sampling overhead (number of shots needed, relative to no mitigation)
    overhead = (1 / (1 - p)) ** n_gates
    # More precisely, the variance scales as this factor squared
    variance_overhead = ((1 + 2*p) / (1 - 2*p/3)) ** n_gates

    print(f"  {n_gates:3d} CX gates: "
          f"sampling overhead ≈ {overhead:12.1f}x  "
          f"(variance ≈ {variance_overhead:12.1f}x)")

print(f"\nPEC gives unbiased estimates but requires exponentially more shots.")
print(f"Practical limit: ~50-100 noisy gates before overhead is prohibitive.")
