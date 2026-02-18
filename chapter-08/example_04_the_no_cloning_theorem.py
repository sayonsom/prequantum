"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.1 The No-Cloning Theorem
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_04_the_no_cloning_theorem.py
"""

import numpy as np

# PROOF BY CONTRADICTION (in code)
# Assume a cloner U exists such that:
#   U(|ψ⟩ ⊗ |0⟩) = |ψ⟩ ⊗ |ψ⟩  for all |ψ⟩
#
# For |0⟩: U(|0⟩⊗|0⟩) = |0⟩⊗|0⟩ = |00⟩
# For |1⟩: U(|1⟩⊗|0⟩) = |1⟩⊗|1⟩ = |11⟩
#
# For |+⟩ = (|0⟩+|1⟩)/√2:
# By LINEARITY of U (all quantum gates are linear):
#   U(|+⟩⊗|0⟩) = U((|0⟩+|1⟩)/√2 ⊗ |0⟩)
#               = (U(|0⟩⊗|0⟩) + U(|1⟩⊗|0⟩)) / √2
#               = (|00⟩ + |11⟩) / √2    ← Bell state!
#
# But we NEED: |+⟩⊗|+⟩ = (|00⟩+|01⟩+|10⟩+|11⟩)/2
#
# (|00⟩+|11⟩)/√2  ≠  (|00⟩+|01⟩+|10⟩+|11⟩)/2
# Contradiction. No such U exists.

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)

# What linearity gives us
linear_result = (np.kron(ket_0, ket_0) + np.kron(ket_1, ket_1)) / np.sqrt(2)

# What cloning requires
clone_result = np.kron(ket_plus, ket_plus)

print(f"Linearity produces: {np.round(linear_result, 4)}")
print(f"Cloning requires:   {np.round(clone_result, 4)}")
print(f"Equal? {np.allclose(linear_result, clone_result)}")  # False

# The inner product proves it:
overlap = np.dot(linear_result.conj(), clone_result)
print(f"⟨linear|clone⟩ = {overlap:.4f}")  # Not 1 → different states

# DEEPER: the inner product argument (Wootters-Zurek, 1982)
# If U clones |ψ⟩ and |φ⟩:
#   ⟨ψ|φ⟩ = ⟨ψ⊗0|U†U|φ⊗0⟩ = ⟨ψ⊗ψ|φ⊗φ⟩ = (⟨ψ|φ⟩)²
# So ⟨ψ|φ⟩ = (⟨ψ|φ⟩)²  →  ⟨ψ|φ⟩ = 0 or 1
# Meaning U can only clone states that are IDENTICAL or ORTHOGONAL.

# Let's verify this algebraic constraint:
for label, psi, phi_state in [
    ("|0⟩,|1⟩", ket_0, ket_1),
    ("|0⟩,|+⟩", ket_0, ket_plus),
    ("|+⟩,|−⟩", ket_plus, (ket_0 - ket_1)/np.sqrt(2)),
]:
    ip = np.dot(psi.conj(), phi_state)
    print(f"  ⟨{label}⟩ = {ip:.4f},  (⟨ψ|φ⟩)² = {ip**2:.4f},  "
          f"equal? {np.isclose(ip, ip**2)}")
