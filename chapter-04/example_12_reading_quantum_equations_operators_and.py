"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.4 Reading Quantum Equations: Operators and Composition
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_12_reading_quantum_equations_operators_and.py
"""

print("=== Rosetta Stone: Chapter 4 ===\n")

rosetta = [
    ("State 'definitely 0'",       "np.array([1, 0])",         "|0⟩"),
    ("State 'definitely 1'",       "np.array([0, 1])",         "|1⟩"),
    ("Equal superposition",        "(ket_0 + ket_1) / √2",    "|+⟩"),
    ("Conjugate transpose",        "state.conj()",             "⟨ψ|"),
    ("Inner product",              "np.dot(a.conj(), b)",      "⟨a|b⟩"),
    ("Measurement probability",    "|np.dot(a.conj(), b)|²",   "|⟨a|b⟩|²"),
    ("Combine two qubits",         "np.kron(a, b)",            "|a⟩ ⊗ |b⟩"),
    ("Both qubits zero",           "np.kron(ket_0, ket_0)",    "|00⟩"),
    ("Apply gate to state",        "gate @ state",             "U|ψ⟩"),
    ("H on qubit 0, 2-q system",   "np.kron(H, I) @ state",   "(H ⊗ I)|ψ⟩"),
]

for eng, py, math in rosetta:
    print(f"  {eng:36s} | {py:30s} | {math}")
