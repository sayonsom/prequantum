"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.2 The Diffusion Operator: Reflect About the Mean
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_04_the_diffusion_operator_reflect_about_the.py
"""

import numpy as np

# Verify: D acts as "reflect about mean" on any vector
N = 8
D = np.full((N, N), 2/N) - np.eye(N)

# Arbitrary amplitude vector (not normalized -- just to show the reflection)
amps = np.array([0.3, 0.4, -0.5, 0.2, 0.1, 0.6, -0.3, 0.2])
mean = np.mean(amps)
reflected = 2 * mean - amps  # "reflect about mean" formula

# Compare with matrix multiplication
D_result = D @ amps

print(f"Mean = {mean:.4f}")
print(f"{'Amplitude':>10}  {'2*mean - a':>10}  {'D @ a':>10}  {'Match?':>6}")
for i in range(N):
    match = np.isclose(reflected[i], D_result[i])
    print(f"  {amps[i]:+.4f}    {reflected[i]:+.4f}    {D_result[i]:+.4f}    {'yes' if match else 'NO'}")
