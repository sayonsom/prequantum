"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.3 Multi-Qubit Circuits and the Gate Library
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_08_multi_qubit_circuits_and_the_gate_librar.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# === All four Bell states in Qiskit ===
sim = AerSimulator()

bell_circuits = {}

# Phi+: H on q0, CNOT
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
bell_circuits["Phi+"] = qc

# Phi-: X on q0, H on q0, CNOT
qc = QuantumCircuit(2, 2)
qc.x(0)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
bell_circuits["Phi-"] = qc

# Psi+: H on q0, CNOT, X on q1
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.x(1)
qc.measure([0, 1], [0, 1])
bell_circuits["Psi+"] = qc

# Psi-: X on q0, H on q0, CNOT, X on q1
qc = QuantumCircuit(2, 2)
qc.x(0)
qc.h(0)
qc.cx(0, 1)
qc.x(1)
qc.measure([0, 1], [0, 1])
bell_circuits["Psi-"] = qc

for name, circ in bell_circuits.items():
    result = sim.run(circ, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()
    print(f"{name}: {dict(sorted(counts.items()))}")

# Phi+: {'00': ~5000, '11': ~5000}
# Phi-: {'00': ~5000, '11': ~5000}
# Psi+: {'01': ~5000, '10': ~5000}
# Psi-: {'01': ~5000, '10': ~5000}
