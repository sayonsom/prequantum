"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.10 Circuit Composition and Reuse
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_27_circuit_composition_and_reuse.py
"""

from qiskit import QuantumCircuit

# compose() merges two circuits
qc1 = QuantumCircuit(3)
qc1.h(0)
qc1.cx(0, 1)

qc2 = QuantumCircuit(3)
qc2.cx(1, 2)
qc2.h(2)

# Compose: qc2 applied after qc1
combined = qc1.compose(qc2)
print("Composed circuit:")
print(combined.draw())

# Compose with qubit mapping: apply qc2's qubit 0,1 to main's qubit 1,2
partial = QuantumCircuit(3)
partial.h(0)

sub = QuantumCircuit(2)
sub.cx(0, 1)

composed = partial.compose(sub, qubits=[1, 2])
print("\nPartially composed:")
print(composed.draw())
