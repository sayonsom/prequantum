"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.1 The No-Cloning Theorem
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_03_the_no_cloning_theorem.py
"""

import numpy as np

# Can we build a unitary U such that:
# U(|ψ⟩ ⊗ |0⟩) = |ψ⟩ ⊗ |ψ⟩  for ALL |ψ⟩?

# Let's try. If it works for |0⟩ and |1⟩:
# U(|0⟩ ⊗ |0⟩) = |0⟩ ⊗ |0⟩ = |00⟩
# U(|1⟩ ⊗ |0⟩) = |1⟩ ⊗ |1⟩ = |11⟩

# That's just CNOT! Let's check:
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Clone |0⟩
input_00 = np.kron(ket_0, ket_0)
result = CNOT @ input_00
print(f"CNOT|00⟩ = {result}")  # [1, 0, 0, 0] = |00⟩ ✓ "cloned" |0⟩

# Clone |1⟩
input_10 = np.kron(ket_1, ket_0)
result = CNOT @ input_10
print(f"CNOT|10⟩ = {result}")  # [0, 0, 0, 1] = |11⟩ ✓ "cloned" |1⟩

# Now try to clone |+⟩ = (|0⟩ + |1⟩)/√2
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
input_plus_0 = np.kron(ket_plus, ket_0)
result = CNOT @ input_plus_0
print(f"\nCNOT(|+⟩ ⊗ |0⟩) = {np.round(result, 4)}")
# [0.7071, 0, 0, 0.7071] = (|00⟩ + |11⟩)/√2 = Bell Phi+

# What we WANTED: |+⟩ ⊗ |+⟩
wanted = np.kron(ket_plus, ket_plus)
print(f"|+⟩ ⊗ |+⟩        = {np.round(wanted, 4)}")
# [0.5, 0.5, 0.5, 0.5]

print(f"\nMatch? {np.allclose(result, wanted)}")  # False!
# We got an ENTANGLED state, not two independent copies.
