"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_12_break_this.py
"""

import numpy as np

# Calibration matrix (rows = read outcome, cols = true state)
# P(read 0 | true 0) = 0.95, P(read 0 | true 1) = 0.03
# P(read 1 | true 0) = 0.05, P(read 1 | true 1) = 0.97
M = np.array([
    [0.95, 0.03],
    [0.05, 0.97]
])

# Noisy measurement result: 60% zeros, 40% ones
noisy_probs = np.array([0.60, 0.40])

# BUG: multiplying by M instead of M_inverse
# M @ ideal = noisy, so ideal = M_inv @ noisy
mitigated = M @ noisy_probs  # WRONG: should be np.linalg.inv(M) @ noisy_probs

print(f"Noisy:     {noisy_probs}")
print(f"Mitigated: {np.round(mitigated, 4)}")
# The mitigated probabilities don't make sense!
