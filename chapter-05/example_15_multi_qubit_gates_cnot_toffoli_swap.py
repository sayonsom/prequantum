"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.7 Multi-Qubit Gates: CNOT, Toffoli, SWAP
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_15_multi_qubit_gates_cnot_toffoli_swap.py
"""

import numpy as np

# Toffoli: 8x8 matrix (3 qubits = 2³ = 8 amplitudes)
# Only |110⟩ ↔ |111⟩ are swapped; everything else unchanged
Toffoli = np.eye(8, dtype=complex)
Toffoli[6, 6] = 0  # |110⟩ row
Toffoli[7, 7] = 0  # |111⟩ row
Toffoli[6, 7] = 1  # |110⟩ ← |111⟩
Toffoli[7, 6] = 1  # |111⟩ ← |110⟩

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Test: both controls = 1, target = 0 → target flips to 1
state_110 = np.kron(np.kron(ket_1, ket_1), ket_0)
result = Toffoli @ state_110
out_idx = np.argmax(np.abs(result))
print(f"Toffoli|110⟩ = |{format(out_idx, '03b')}⟩")  # |111⟩ ← target flipped!

# Test: one control = 0 → target unchanged
state_100 = np.kron(np.kron(ket_1, ket_0), ket_0)
result = Toffoli @ state_100
out_idx = np.argmax(np.abs(result))
print(f"Toffoli|100⟩ = |{format(out_idx, '03b')}⟩")  # |100⟩ ← unchanged

# Toffoli is unitary and self-inverse
print(f"\nToffoli is unitary: {np.allclose(Toffoli @ Toffoli.conj().T, np.eye(8))}")
print(f"Toffoli² = I: {np.allclose(Toffoli @ Toffoli, np.eye(8))}")
