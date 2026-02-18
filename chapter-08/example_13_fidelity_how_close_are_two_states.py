"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.5 Fidelity: How Close Are Two States?
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_13_fidelity_how_close_are_two_states.py
"""

import numpy as np
from qiskit.quantum_info import Statevector, state_fidelity

# Trace distance from fidelity (for pure states, D = √(1-F))
def trace_distance_from_fidelity(F):
    """Trace distance for pure states: D = √(1 - F)."""
    return np.sqrt(1 - F)

# Example: how distinguishable are |0⟩ and |+⟩?
sv_0 = Statevector.from_label('0')
sv_plus = Statevector.from_label('+')
F = state_fidelity(sv_0, sv_plus)
D = trace_distance_from_fidelity(F)
print(f"|0⟩ vs |+⟩:  F = {F:.4f},  D = {D:.4f}")
print(f"  You can distinguish them with probability at most {0.5 + D/2:.4f}")

# Near-identical states
theta = 0.05
sv_near = Statevector([np.cos(theta/2), np.sin(theta/2)])
F = state_fidelity(sv_0, sv_near)
D = trace_distance_from_fidelity(F)
print(f"\n|0⟩ vs Ry(0.05)|0⟩:  F = {F:.6f},  D = {D:.6f}")
print(f"  Nearly indistinguishable: {0.5 + D/2:.6f} success probability (0.5 = random)")
