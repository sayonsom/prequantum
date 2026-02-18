"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.1 Anatomy of a Quantum Circuit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_02_anatomy_of_a_quantum_circuit.py
"""

from qiskit import QuantumCircuit

# Create a circuit: 2 quantum bits, 2 classical bits
qc = QuantumCircuit(2, 2)

# Qubits start in state |0⟩ by default
# Apply gates (operations flow left to right)
qc.h(0)          # Hadamard on qubit 0
qc.cx(0, 1)      # CNOT: control=0, target=1
qc.measure(0, 0)  # Measure qubit 0 → classical bit 0
qc.measure(1, 1)  # Measure qubit 1 → classical bit 1

print(qc.draw())
#      ┌───┐     ┌─┐
# q_0: ┤ H ├──■──┤M├───
#      └───┘┌─┴─┐└╥┘┌─┐
# q_1: ────┤ X ├─╫─┤M├
#           └───┘ ║ └╥┘
# c: 2/══════════╩══╩═
#                 0  1
