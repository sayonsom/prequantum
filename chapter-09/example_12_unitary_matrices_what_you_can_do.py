"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.9 Unitary Matrices: What You Can Do
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_12_unitary_matrices_what_you_can_do.py
"""

import numpy as np

# ─── UNITARY MATRICES: U†U = I ───
# "Conjugate transpose is the inverse"
# These represent GATES (operations that evolve states)
Z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
X_gate = np.array([[0, 1], [1, 0]], dtype=complex)
H_gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

print(f"Z†Z = I? {np.allclose(Z_gate.conj().T @ Z_gate, np.eye(2))}")  # True → Unitary
print(f"X†X = I? {np.allclose(X_gate.conj().T @ X_gate, np.eye(2))}")  # True → Unitary
print(f"H†H = I? {np.allclose(H_gate.conj().T @ H_gate, np.eye(2))}")  # True → Unitary

# Wait -- Z, X, H are BOTH Hermitian AND Unitary?
# Yes! Some matrices are both. But not all.

# S gate: unitary but NOT Hermitian
S_gate = np.array([[1, 0], [0, 1j]], dtype=complex)
print(f"\nS†S = I?  {np.allclose(S_gate.conj().T @ S_gate, np.eye(2))}")  # True → Unitary
print(f"S† = S?   {np.allclose(S_gate.conj().T, S_gate)}")                # False → NOT Hermitian

# T gate: unitary but NOT Hermitian
T_gate = np.array([[1, 0], [0, np.exp(1j * np.pi/4)]], dtype=complex)
print(f"T†T = I?  {np.allclose(T_gate.conj().T @ T_gate, np.eye(2))}")  # True → Unitary
print(f"T† = T?   {np.allclose(T_gate.conj().T, T_gate)}")                # False → NOT Hermitian

# ─── WHY UNITARITY PRESERVES PROBABILITY ───
U = H_gate  # Hadamard
psi = np.array([0.6+0j, 0.8+0j])

# Probability before gate
prob_before = np.dot(psi.conj(), psi)
print(f"\nTotal probability before: {prob_before.real:.4f}")  # 1.0

# Apply gate
psi_after = U @ psi
prob_after = np.dot(psi_after.conj(), psi_after)
print(f"Total probability after:  {prob_after.real:.4f}")  # 1.0

# WHY? Because:
# ⟨ψ'|ψ'⟩ = ⟨Uψ|Uψ⟩ = ⟨ψ|U†U|ψ⟩ = ⟨ψ|I|ψ⟩ = ⟨ψ|ψ⟩ = 1
# The U†U = I property guarantees this.

# ─── NON-UNITARY MATRIX: BREAKS PROBABILITY ───
bad_gate = np.array([[2, 0], [0, 1]], dtype=complex)  # NOT unitary
print(f"\nbad_gate†·bad_gate = I? {np.allclose(bad_gate.conj().T @ bad_gate, np.eye(2))}")

psi_broken = bad_gate @ psi
prob_broken = np.dot(psi_broken.conj(), psi_broken)
print(f"Probability after bad gate: {prob_broken.real:.4f}")  # 1.64 ≠ 1 → not physical!
