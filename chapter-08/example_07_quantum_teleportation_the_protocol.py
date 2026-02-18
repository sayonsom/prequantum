"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.3 Quantum Teleportation: The Protocol
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_07_quantum_teleportation_the_protocol.py
"""

import numpy as np
from fractions import Fraction

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I = np.eye(2, dtype=complex)

# The state to teleport (Alice doesn't know these values)
alpha = 0.6 + 0j
beta = 0.8 + 0j
psi = alpha * ket_0 + beta * ket_1
print(f"State to teleport |ψ⟩ = {np.round(psi, 4)}")

# STEP 0: Initial state = |ψ⟩ ⊗ |Φ+⟩
# Expand: (α|0⟩ + β|1⟩) ⊗ (|00⟩ + |11⟩)/√2
# = (α|000⟩ + α|011⟩ + β|100⟩ + β|111⟩) / √2
bell = (np.kron(ket_0, ket_0) + np.kron(ket_1, ket_1)) / np.sqrt(2)
state = np.kron(psi, bell)  # 8-element vector (3 qubits)
print(f"\nSTEP 0 - Initial |ψ⟩⊗|Φ+⟩:")
labels = ['000','001','010','011','100','101','110','111']
for i, (amp, lab) in enumerate(zip(state, labels)):
    if abs(amp) > 1e-10:
        print(f"  {amp:+.4f} |{lab}⟩")

# STEP 1: Alice applies CNOT (control=q0, target=q1)
# |000⟩ → |000⟩, |011⟩ → |011⟩, |100⟩ → |110⟩, |111⟩ → |101⟩
CNOT_01 = np.kron(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex), I)
state = CNOT_01 @ state
print(f"\nSTEP 1 - After CNOT(q0→q1):")
for amp, lab in zip(state, labels):
    if abs(amp) > 1e-10:
        print(f"  {amp:+.4f} |{lab}⟩")

# STEP 2: Alice applies H to qubit 0
# |0⟩ → (|0⟩+|1⟩)/√2,  |1⟩ → (|0⟩-|1⟩)/√2
H_on_q0 = np.kron(np.kron(H, I), I)
state = H_on_q0 @ state
print(f"\nSTEP 2 - After H(q0):")
for amp, lab in zip(state, labels):
    if abs(amp) > 1e-10:
        print(f"  {amp:+.4f} |{lab}⟩")

# STEP 3: Regroup by Alice's measurement outcomes (qubits 0,1)
print(f"\nSTEP 3 - Regrouped by Alice's measurement:")
corrections = {
    (0, 0): ("I (nothing)", I),
    (0, 1): ("X", X),
    (1, 0): ("Z", Z),
    (1, 1): ("ZX", Z @ X),
}

for (m0, m1), (name, correction) in corrections.items():
    # Extract Bob's qubit for this outcome
    idx_base = m0 * 4 + m1 * 2
    bob_state = state[idx_base:idx_base + 2]
    bob_norm = np.linalg.norm(bob_state)
    bob_state_normalized = bob_state / bob_norm

    # Apply correction
    corrected = correction @ bob_state_normalized

    print(f"  Alice gets |{m0}{m1}⟩: Bob has {np.round(bob_state_normalized, 4)}")
    print(f"    → Apply {name:10s} → {np.round(corrected, 4)}  "
          f"(matches |ψ⟩? {np.allclose(corrected, psi) or np.allclose(corrected, -psi)})")

print(f"\nOriginal state: {np.round(psi, 4)}")
print("All four corrections recover |ψ⟩ (up to global phase).")
