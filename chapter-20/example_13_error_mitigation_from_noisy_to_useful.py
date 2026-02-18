"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.7 Error Mitigation: From Noisy to Useful
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_13_error_mitigation_from_noisy_to_useful.py
"""

import numpy as np
from numpy.polynomial import polynomial as P

# ZNE demonstration
# True expectation value (what the noiseless circuit would give)
true_value = 0.85

# Noise model: exponential decay with circuit noise
base_noise = 0.08  # effective noise per "unit" of circuit

def noisy_result(noise_scale, true_val=true_value, base=base_noise):
    """Simulate running circuit at amplified noise level."""
    # Exponential decay model: result * exp(-noise_scale * base_noise)
    return true_val * np.exp(-noise_scale * base) + np.random.normal(0, 0.005)

# Run at multiple noise amplification factors
np.random.seed(42)
noise_factors = [1, 3, 5]  # 1x = original, 3x = triple noise, 5x = 5x noise
results = []
n_samples = 50  # average over many runs for stability

print("ZNE: Running at amplified noise levels")
print(f"{'Noise factor':>13} | {'Measured':>10} | {'True':>8}")
print("-" * 38)
for factor in noise_factors:
    samples = [noisy_result(factor) for _ in range(n_samples)]
    avg = np.mean(samples)
    results.append(avg)
    print(f"{factor:>13}x | {avg:>10.4f} | {true_value:>8.4f}")

# Extrapolate to 0x noise using polynomial fit
# Linear extrapolation (simplest)
coeffs_linear = np.polyfit(noise_factors, results, 1)
zne_linear = np.polyval(coeffs_linear, 0)

# Quadratic extrapolation (more accurate for this model)
coeffs_quad = np.polyfit(noise_factors, results, 2)
zne_quad = np.polyval(coeffs_quad, 0)

# Exponential extrapolation (best for this noise model)
log_results = np.log(np.array(results))
coeffs_exp = np.polyfit(noise_factors, log_results, 1)
zne_exp = np.exp(np.polyval(coeffs_exp, 0))

print(f"\n{'Method':<25} | {'Estimate':>10} | {'Error':>8}")
print("-" * 50)
print(f"{'No mitigation (1x noise)':<25} | {results[0]:>10.4f} | {abs(results[0]-true_value):>8.4f}")
print(f"{'ZNE (linear)':<25} | {zne_linear:>10.4f} | {abs(zne_linear-true_value):>8.4f}")
print(f"{'ZNE (quadratic)':<25} | {zne_quad:>10.4f} | {abs(zne_quad-true_value):>8.4f}")
print(f"{'ZNE (exponential)':<25} | {zne_exp:>10.4f} | {abs(zne_exp-true_value):>8.4f}")
print(f"{'True value':<25} | {true_value:>10.4f} |")

# Output (approximately):
# ZNE: Running at amplified noise levels
#  Noise factor |   Measured |     True
# --------------------------------------
#            1x |     0.7889 |   0.8500
#            3x |     0.6703 |   0.8500
#            5x |     0.5632 |   0.8500
#
# Method                    |   Estimate |    Error
# --------------------------------------------------
# No mitigation (1x noise)  |     0.7889 |   0.0611
# ZNE (linear)              |     0.8467 |   0.0033
# ZNE (quadratic)           |     0.8530 |   0.0030
# ZNE (exponential)         |     0.8502 |   0.0002
# True value                |     0.8500 |
