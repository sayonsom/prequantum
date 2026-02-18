"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.6 The Outer Product: Building Operators from States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_09_the_outer_product_building_operators_fro.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# INNER product: vector × vector → scalar
inner = np.dot(ket_0.conj(), ket_1)
print(f"⟨0|1⟩ = {inner}")  # 0 (a number)

# OUTER product: vector × vector → matrix
outer = np.outer(ket_0, ket_1.conj())
print(f"\n|0⟩⟨1| =")
print(outer)
# [[0, 1],
#  [0, 0]]  (a 2×2 matrix)

# The outer product |ψ⟩⟨ψ| is a PROJECTION operator.
# It projects any state onto the |ψ⟩ direction.
proj_0 = np.outer(ket_0, ket_0.conj())
print(f"\n|0⟩⟨0| (projector onto |0⟩):")
print(proj_0)
# [[1, 0],
#  [0, 0]]

# Apply it: project a general state onto |0⟩
psi = np.array([0.6+0j, 0.8+0j])
projected = proj_0 @ psi
print(f"\n|0⟩⟨0| @ |ψ⟩ = {projected}")  # [0.6, 0] -- only the |0⟩ component survives

# Projection onto |+⟩
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
proj_plus = np.outer(ket_plus, ket_plus.conj())
print(f"\n|+⟩⟨+| (projector onto |+⟩):")
print(np.round(proj_plus, 4))

projected_plus = proj_plus @ psi
print(f"|+⟩⟨+| @ |ψ⟩ = {np.round(projected_plus, 4)}")
