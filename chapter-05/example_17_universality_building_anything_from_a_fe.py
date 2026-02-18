"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.8 Universality: Building Anything from a Few Gates
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_17_universality_building_anything_from_a_fe.py
"""

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
I = np.eye(2, dtype=complex)

print("=== Quantum Gate Cheat Sheet ===\n")

gates = [
    ("I  (identity)",    I,  "Do nothing",            "—"),
    ("X  (Pauli-X/NOT)", X,  "Bit flip: |0⟩↔|1⟩",   "HT⁴H"),
    ("Y  (Pauli-Y)",     Y,  "Bit + phase flip",      "iXZ"),
    ("Z  (Pauli-Z)",     Z,  "Phase flip: |1⟩→−|1⟩", "T⁴"),
    ("H  (Hadamard)",    H,  "Basis change: |0⟩↔|+⟩", "fundamental"),
    ("S  (Phase-π/2)",   S,  "|1⟩ → i|1⟩",           "T²"),
    ("T  (Phase-π/4)",   T,  "|1⟩ → e^(iπ/4)|1⟩",   "fundamental"),
]

for name, gate, desc, recipe in gates:
    unitary = np.allclose(gate @ gate.conj().T, np.eye(2))
    self_inv = np.allclose(gate @ gate, np.eye(2))
    inv_str = "self-inverse" if self_inv else "not self-inverse"
    print(f"  {name:20s} {desc:28s} Built from: {recipe:12s} ({inv_str})")
