"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.7 Error Mitigation: Making Noisy Results Trustworthy
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_08_error_mitigation_making_noisy_results_tr.py
"""

import numpy as np

# Simulate noisy expectation values with zero-noise extrapolation (ZNE)
# ZNE idea: run the circuit at several noise levels, extrapolate to zero noise.

def noisy_expectation(exact_value, noise_rate):
    """Simulate a noisy expectation value.

    A simple noise model: the expectation value decays exponentially
    toward 0 (the maximally mixed state) as noise increases.
    ⟨O⟩_noisy ≈ ⟨O⟩_exact × exp(-λ × noise_rate)
    Plus some statistical noise from finite shots.
    """
    decay = np.exp(-1.5 * noise_rate)
    shot_noise = np.random.normal(0, 0.02)
    return exact_value * decay + shot_noise

# True expectation value (unknown in practice)
exact_value = -1.35

# Step 1: Measure at the base noise rate (what the hardware gives you)
base_noise = 1.0  # normalized
e_base = noisy_expectation(exact_value, base_noise)

# Step 2: Amplify noise by factors c = 1, 3, 5
# On real hardware, you do this by inserting identity gates as G G† pairs
# (gate folding) or by probabilistic error amplification (PEA).
noise_factors = [1.0, 3.0, 5.0]
noisy_values = []
print("ZNE: noise-amplified measurements")
for c in noise_factors:
    val = noisy_expectation(exact_value, c * base_noise)
    noisy_values.append(val)
    print(f"  noise factor c={c:.1f}: ⟨O⟩ = {val:.4f}")

# Step 3: Extrapolate to zero noise (c=0) using polynomial fit
# Richardson extrapolation (linear)
coeffs = np.polyfit(noise_factors, noisy_values, deg=min(2, len(noise_factors)-1))
zne_estimate = np.polyval(coeffs, 0.0)

print(f"\nZNE extrapolated value: {zne_estimate:.4f}")
print(f"Exact value:            {exact_value:.4f}")
print(f"Unmitigated (c=1):      {noisy_values[0]:.4f}")
print(f"ZNE error:              {abs(zne_estimate - exact_value):.4f}")
print(f"Unmitigated error:      {abs(noisy_values[0] - exact_value):.4f}")

# --- Probabilistic Error Cancellation (PEC) ---
# PEC is more powerful but more expensive.
# Idea: learn the noise channel, then construct a quasi-probability
# distribution over noisy circuits that inverts the noise.
#
# If the noise channel is N, PEC finds coefficients {q_i} such that
# Σ q_i N_i = N^{-1} (the inverse noise channel).
# The q_i can be negative → "quasi-probability" → requires sampling overhead.
#
# Sampling overhead scales as γ² where γ = Σ|q_i| ≥ 1.
# For a circuit with d noisy layers: γ_total = γ_per_layer^d
# → exponential in circuit depth. This limits PEC to shallow circuits.

print(f"\n--- PEC cost scaling ---")
gamma_per_layer = 1.05  # typical for a good gate (99% fidelity)
for depth in [10, 50, 100, 200]:
    overhead = gamma_per_layer ** (2 * depth)
    print(f"  depth={depth:3d}: sampling overhead = {overhead:.1e}x")
print(f"  PEC is practical for depth < ~50 with current gate fidelities")
