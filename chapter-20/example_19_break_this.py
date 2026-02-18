"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_19_break_this.py
"""

import numpy as np

# Confusion matrix: M[i][j] = P(measure i | prepared j)
M = np.array([
    [0.95, 0.05],
    [0.03, 0.97],
])

# Measured probabilities from hardware
measured = np.array([0.62, 0.38])

# Bug 1: multiplying instead of inverting
mitigated = M @ measured

# Bug 2: no clipping or renormalization
print(f"Mitigated: {mitigated}")
# Output: [0.608, 0.387] -- barely changed and doesn't sum to 1!
