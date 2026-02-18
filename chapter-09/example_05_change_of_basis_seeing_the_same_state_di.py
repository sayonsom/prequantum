"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.4 Change of Basis: Seeing the Same State Differently
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_05_change_of_basis_seeing_the_same_state_di.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

# Change of basis matrix: columns are the NEW basis vectors
# in terms of the OLD basis
# To go FROM Hadamard TO computational, columns are |+⟩ and |−⟩:
P = np.column_stack([ket_plus, ket_minus])
print(f"Change of basis matrix P:")
print(np.round(P, 4))
# This IS the Hadamard matrix!

# To go FROM computational TO Hadamard, use P† (conjugate transpose)
P_dagger = P.conj().T
print(f"\nP† (comp → Hadamard):")
print(np.round(P_dagger, 4))
# Also the Hadamard matrix! (because H = H†)

# Transform a state
psi_comp = np.array([0.6+0j, 0.8+0j])
psi_had = P_dagger @ psi_comp
print(f"\n|ψ⟩ in computational: {np.round(psi_comp, 4)}")
print(f"|ψ⟩ in Hadamard:      {np.round(psi_had, 4)}")

# Verify: P† @ P = I (unitary!)
print(f"\nP† @ P = I? {np.allclose(P_dagger @ P, np.eye(2))}")
