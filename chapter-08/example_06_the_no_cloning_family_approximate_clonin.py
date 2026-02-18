"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.2 The No-Cloning Family: Approximate Cloning and No-Deleting
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_06_the_no_cloning_family_approximate_clonin.py
"""

import numpy as np

# No-deleting theorem (Pati & Braunstein, 2000):
# No unitary U can achieve: U(|ψ⟩ ⊗ |ψ⟩) = |ψ⟩ ⊗ |0⟩ for all |ψ⟩
#
# Proof sketch (same inner product trick):
# If U deletes for |ψ⟩ and |φ⟩:
#   ⟨ψ|φ⟩² = ⟨ψ⊗ψ|φ⊗φ⟩ = ⟨ψ⊗0|U†U|φ⊗0⟩ = ⟨ψ|φ⟩ · 1
# So (⟨ψ|φ⟩)² = ⟨ψ|φ⟩ → ⟨ψ|φ⟩ = 0 or 1. Same constraint as no-cloning.

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)

# Try to build a "deleter" for |+⟩⊗|+⟩ → |+⟩⊗|0⟩
# Start with |+⟩⊗|+⟩
two_plus = np.kron(ket_plus, ket_plus)
target = np.kron(ket_plus, ket_0)

# These have different inner product structures:
print(f"|+⟩⊗|+⟩ = {np.round(two_plus, 4)}")
print(f"|+⟩⊗|0⟩ = {np.round(target, 4)}")
print(f"Same state? {np.allclose(two_plus, target)}")  # False

# The no-cloning / no-deleting pair tells us:
# Quantum information is CONSERVED by unitary evolution.
# You can MOVE it (teleportation), TRANSFORM it (gates),
# but not CREATE or DESTROY it.
print("\nQuantum information conservation:")
print("  Cannot create copies  (no-cloning)")
print("  Cannot erase copies   (no-deleting)")
print("  CAN move it           (teleportation)")
print("  CAN transform it      (unitary gates)")
