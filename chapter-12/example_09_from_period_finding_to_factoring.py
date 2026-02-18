"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.6 From Period Finding to Factoring
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_09_from_period_finding_to_factoring.py
"""

import numpy as np
from fractions import Fraction

# The connection: QPE eigenvalue phases → period
# The unitary U|y⟩ = |ay mod N⟩ has eigenvalues e^(2πis/r)
# for s = 0, 1, ..., r-1. QPE measures s/r.

# For a=7, N=15: period r=4
# Eigenvalue phases: 0/4, 1/4, 2/4, 3/4

# From the Quick Win, we measured phases:
measured_phases = [0/8, 2/8, 4/8, 6/8]  # 0, 0.25, 0.5, 0.75

print("Measured phases → period extraction via continued fractions:")
for phase in measured_phases:
    if phase == 0:
        print(f"  φ = {phase:.4f} → s/r = 0 (trivial, skip)")
        continue
    # Use continued fractions to find r from s/r
    frac = Fraction(phase).limit_denominator(15)
    print(f"  φ = {phase:.4f} → s/r ≈ {frac} → r = {frac.denominator}")

print(f"\nAll non-trivial phases give r = 4")
print(f"Check: 7^4 mod 15 = {pow(7, 4, 15)}")
print(f"gcd(7^2 - 1, 15) = gcd({7**2 - 1}, 15) = {np.gcd(7**2 - 1, 15)}")
print(f"gcd(7^2 + 1, 15) = gcd({7**2 + 1}, 15) = {np.gcd(7**2 + 1, 15)}")
print(f"15 = 3 × 5")

# Continued fractions in detail: why they recover r from approximate s/r
print("\n--- Continued Fractions Deep Dive ---")
print("Given approximate phase 0.74902... (noisy estimate of 3/4):")

noisy_phase = 0.74902
cf_convergents = []
x = noisy_phase
for i in range(8):
    a_i = int(x)
    cf_convergents.append(a_i)
    remainder = x - a_i
    if abs(remainder) < 1e-10:
        break
    x = 1 / remainder

print(f"  Continued fraction coefficients: {cf_convergents}")

# Reconstruct convergents
from fractions import Fraction
for max_denom in [4, 15, 100]:
    frac = Fraction(noisy_phase).limit_denominator(max_denom)
    print(f"  limit_denominator({max_denom}): {frac} → r = {frac.denominator}")
