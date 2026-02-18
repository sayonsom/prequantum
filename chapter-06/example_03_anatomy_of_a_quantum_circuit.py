"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.1 Anatomy of a Quantum Circuit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_03_anatomy_of_a_quantum_circuit.py
"""

from qiskit import QuantumCircuit

# Circuit metadata
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

print(f"Number of qubits: {qc.num_qubits}")        # 2
print(f"Number of classical bits: {qc.num_clbits}") # 2
print(f"Circuit depth: {qc.depth()}")                # 3 (H, CX, measure)
print(f"Gate counts: {dict(qc.count_ops())}")        # {'h': 1, 'cx': 1, 'measure': 2}
