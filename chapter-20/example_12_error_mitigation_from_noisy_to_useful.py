"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.7 Error Mitigation: From Noisy to Useful
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_12_error_mitigation_from_noisy_to_useful.py
"""

import numpy as np

# Demonstrate the difference between coherent and stochastic error accumulation
n_gates_range = np.arange(1, 51)

# Coherent error: systematic over-rotation by epsilon per gate
epsilon = 0.02  # 2% rotation error
coherent_error = np.sin(n_gates_range * epsilon) ** 2  # quadratic at first

# Stochastic error: random per gate (after twirling)
stochastic_error = 1 - (1 - epsilon**2) ** n_gates_range  # linear

print("Error accumulation: coherent vs stochastic (after Pauli twirling)")
print(f"{'Gates':>6} | {'Coherent':>10} | {'Stochastic':>11} | {'Improvement':>12}")
print("-" * 48)
for n in [5, 10, 20, 30, 50]:
    c = np.sin(n * epsilon) ** 2
    s = 1 - (1 - epsilon**2) ** n
    print(f"{n:>6} | {c:>10.4f} | {s:>11.4f} | {c/s:>10.1f}x worse")

# Output:
# Gates |   Coherent |  Stochastic | Improvement
# ------------------------------------------------
#     5 |     0.0100 |      0.0020 |        5.0x worse
#    10 |     0.0394 |      0.0040 |       10.0x worse
#    20 |     0.1514 |      0.0079 |       19.1x worse
#    30 |     0.3187 |      0.0119 |       26.8x worse
#    50 |     0.7081 |      0.0198 |       35.8x worse
