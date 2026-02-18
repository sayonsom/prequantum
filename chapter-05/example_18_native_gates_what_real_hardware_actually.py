"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.9 Native Gates: What Real Hardware Actually Uses
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_18_native_gates_what_real_hardware_actually.py
"""

import numpy as np

# IBM Heron processor native gates (2024-2025):
#   Single-qubit: SX (√X), RZ(θ), X
#   Two-qubit: CZ (controlled-Z)

# SX = square root of X
SX = np.array([
    [0.5 + 0.5j, 0.5 - 0.5j],
    [0.5 - 0.5j, 0.5 + 0.5j]
], dtype=complex)

X = np.array([[0, 1], [1, 0]], dtype=complex)
print(f"SX² = X? {np.allclose(SX @ SX, X)}")  # True
print(f"SX is unitary? {np.allclose(SX @ SX.conj().T, np.eye(2))}")  # True

# How does the transpiler build H from IBM's native gates?
# H = Rz(π/2) · SX · Rz(π/2)  (one possible decomposition)
def Rz(theta):
    return np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)]
    ], dtype=complex)

H_native = Rz(np.pi/2) @ SX @ Rz(np.pi/2)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

# They differ by a global phase, but are functionally identical
probs_match = np.allclose(np.abs(H_native)**2, np.abs(H)**2)
print(f"\nH from native gates has same probabilities? {probs_match}")  # True

# CZ gate (IBM Heron's native 2-qubit gate)
CZ = np.diag([1, 1, 1, -1]).astype(complex)

# Build CNOT from CZ + single-qubit gates:
# CNOT = (I ⊗ H) · CZ · (I ⊗ H)
I2 = np.eye(2, dtype=complex)
IH = np.kron(I2, H)
CNOT_from_CZ = IH @ CZ @ IH
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
print(f"CNOT from CZ: {np.allclose(CNOT_from_CZ, CNOT)}")  # True
