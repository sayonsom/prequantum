"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.3 Multi-Qubit Circuits and the Gate Library
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_10_multi_qubit_circuits_and_the_gate_librar.py
"""

from qiskit import QuantumCircuit

# === Multi-qubit gates ===
# SWAP
qc = QuantumCircuit(2)
qc.swap(0, 1)
print("SWAP circuit:")
print(qc.draw())

# Toffoli (CCX)
qc = QuantumCircuit(3)
qc.ccx(0, 1, 2)  # control=q0,q1, target=q2
print("\nToffoli circuit:")
print(qc.draw())

# Controlled-Z
qc = QuantumCircuit(2)
qc.cz(0, 1)
print("\nControlled-Z circuit:")
print(qc.draw())
