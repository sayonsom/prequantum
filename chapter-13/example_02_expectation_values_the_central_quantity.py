"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.1 Expectation Values: The Central Quantity
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_02_expectation_values_the_central_quantity.py
"""

import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Expectation value: ⟨ψ|H|ψ⟩
# For a single qubit in state |ψ⟩, ⟨ψ|Z|ψ⟩ gives the expected
# value of measuring in the Z basis

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)

# |0⟩: Z-measurement always gives +1
exp_Z_0 = np.real(ket_0.conj() @ Z @ ket_0)
print(f"⟨0|Z|0⟩ = {exp_Z_0:.4f}")  # +1.0

# |1⟩: Z-measurement always gives -1
exp_Z_1 = np.real(ket_1.conj() @ Z @ ket_1)
print(f"⟨1|Z|1⟩ = {exp_Z_1:.4f}")  # -1.0

# |+⟩: Z-measurement gives +1 or -1 with equal probability → average = 0
exp_Z_plus = np.real(ket_plus.conj() @ Z @ ket_plus)
print(f"⟨+|Z|+⟩ = {exp_Z_plus:.4f}")  # 0.0

# Expectation value of X on |0⟩: X-measurement gives +1 or -1 equally → 0
exp_X_0 = np.real(ket_0.conj() @ X @ ket_0)
print(f"⟨0|X|0⟩ = {exp_X_0:.4f}")  # 0.0

# Expectation value of X on |+⟩: X-measurement always gives +1
exp_X_plus = np.real(ket_plus.conj() @ X @ ket_plus)
print(f"⟨+|X|+⟩ = {exp_X_plus:.4f}")  # 1.0

# For a multi-qubit Hamiltonian like H = Z⊗Z + X⊗I,
# ⟨ψ|H|ψ⟩ = ⟨ψ|Z⊗Z|ψ⟩ + ⟨ψ|X⊗I|ψ⟩
# Each term can be measured independently and summed.
bell = (np.kron(ket_0, ket_0) + np.kron(ket_1, ket_1)) / np.sqrt(2)
H_simple = np.kron(Z, Z) + np.kron(X, I)

exp_total = np.real(bell.conj() @ H_simple @ bell)
exp_ZZ = np.real(bell.conj() @ np.kron(Z, Z) @ bell)
exp_XI = np.real(bell.conj() @ np.kron(X, I) @ bell)
print(f"\nBell state |Φ+⟩:")
print(f"  ⟨Φ+|Z⊗Z|Φ+⟩ = {exp_ZZ:.4f}")
print(f"  ⟨Φ+|X⊗I|Φ+⟩ = {exp_XI:.4f}")
print(f"  ⟨Φ+|H|Φ+⟩    = {exp_total:.4f} = {exp_ZZ:.4f} + {exp_XI:.4f}")
