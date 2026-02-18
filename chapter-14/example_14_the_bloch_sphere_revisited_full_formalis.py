"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.6 The Bloch Sphere Revisited: Full Formalism
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_14_the_bloch_sphere_revisited_full_formalis.py
"""

import numpy as np

# Apply noise to |0⟩ (Bloch vector [0, 0, 1]) and track the Bloch vector
def apply_channel_bloch(channel_fn, param, rho):
    """Apply a channel and return the resulting Bloch vector."""
    kraus = channel_fn(param)
    rho_out = sum(K @ rho @ K.conj().T for K in kraus)
    return bloch_vector(rho_out)

# Start with |+⟩ (Bloch vector [1, 0, 0])
rho_plus = density_from_bloch(np.array([1.0, 0.0, 0.0]))

print("Effect of noise channels on |+⟩ (Bloch vector [1, 0, 0]):")
print(f"{'Channel':<20} {'p':>4} | {'r_x':>6} {'r_y':>6} {'r_z':>6} {'|r|':>6}")
print("-" * 56)

for p in [0.0, 0.3, 0.6, 1.0]:
    # Depolarizing: uniform shrinkage → r → (1-p)r
    kraus_dep = depolarizing_channel(p)
    rho_dep = apply_channel(rho_plus, kraus_dep)
    r = bloch_vector(rho_dep)
    print(f"{'Depolarizing':<20} {p:4.1f} | {r[0]:6.3f} {r[1]:6.3f} {r[2]:6.3f} {np.linalg.norm(r):6.3f}")

print()
for p in [0.0, 0.3, 0.6, 1.0]:
    # Phase-flip: shrinks x and y, preserves z
    kraus_pf = phase_flip_channel(p)
    rho_pf = apply_channel(rho_plus, kraus_pf)
    r = bloch_vector(rho_pf)
    print(f"{'Phase-flip':<20} {p:4.1f} | {r[0]:6.3f} {r[1]:6.3f} {r[2]:6.3f} {np.linalg.norm(r):6.3f}")

print()
# Start with |1⟩ for amplitude damping
rho_one = density_from_bloch(np.array([0.0, 0.0, -1.0]))
for gamma in [0.0, 0.3, 0.6, 1.0]:
    kraus_ad = amplitude_damping_channel(gamma)
    rho_ad = apply_channel(rho_one, kraus_ad)
    r = bloch_vector(rho_ad)
    print(f"{'Amp. damping |1⟩':<20} {gamma:4.1f} | {r[0]:6.3f} {r[1]:6.3f} {r[2]:6.3f} {np.linalg.norm(r):6.3f}")
# Depolarizing: uniform shrinkage toward center (all components scaled by 1-p)
# Phase-flip: shrinks x,y components (dephasing), preserves z
# Amplitude damping: pulls z toward +1 (|0⟩), the "ground state attractor"
