"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.5 Fidelity: How Close Are Two States?
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_11_fidelity_how_close_are_two_states.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

def fidelity(psi, phi):
    """Compute fidelity F = |⟨ψ|φ⟩|² between two pure states."""
    return abs(np.dot(psi.conj(), phi))**2

# Identical states → fidelity = 1
print(f"F(|0⟩, |0⟩) = {fidelity(ket_0, ket_0):.4f}")       # 1.0
print(f"F(|+⟩, |+⟩) = {fidelity(ket_plus, ket_plus):.4f}")  # 1.0

# Orthogonal states → fidelity = 0
print(f"F(|0⟩, |1⟩) = {fidelity(ket_0, ket_1):.4f}")       # 0.0
print(f"F(|+⟩, |−⟩) = {fidelity(ket_plus, ket_minus):.4f}") # 0.0

# Partial overlap → fidelity between 0 and 1
print(f"F(|0⟩, |+⟩) = {fidelity(ket_0, ket_plus):.4f}")    # 0.5

# Small error: rotate |0⟩ slightly
theta = 0.1  # small angle
slightly_off = np.array([np.cos(theta/2), np.sin(theta/2)], dtype=complex)
print(f"\nF(|0⟩, Ry(0.1)|0⟩) = {fidelity(ket_0, slightly_off):.6f}")
# Very close to 1 -- small rotation, high fidelity

# For small errors, infidelity ≈ θ²/4
print(f"Infidelity: {1 - fidelity(ket_0, slightly_off):.6f}")
print(f"θ²/4:       {theta**2 / 4:.6f}")
print("Close match -- infidelity is quadratic in the error angle.")
