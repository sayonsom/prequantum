"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.1 The SDK Landscape: Qiskit, Cirq, and PennyLane
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_02_the_sdk_landscape_qiskit_cirq_and_pennyl.py
"""

# === Bell State in Qiskit ===
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
print("Qiskit circuit:")
print(qc.draw())
# Output:
#      ┌───┐     ┌─┐
# q_0: ┤ H ├──■──┤M├───
#      └───┘┌─┴─┐└╥┘┌─┐
# q_1: ────┤ CX ├─╫─┤M├
#           └───┘ ║ └╥┘
# c: 2/══════════╩══╩═
#                0  1

# === Bell State in Cirq ===
import cirq

q0, q1 = cirq.LineQubit.range(2)
circuit_cirq = cirq.Circuit([
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='result')
])
print("\nCirq circuit:")
print(circuit_cirq)
# Output:
# 0: ───H───@───M('result')───
#           │   │
# 1: ───────X───M──────────────

# === Bell State in PennyLane ===
import pennylane as qml

dev = qml.device('default.qubit', wires=2, shots=1024)

@qml.qnode(dev)
def bell_state():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.counts()

print("\nPennyLane result:")
print(bell_state())
# Output: {'00': 512, '11': 512}  (approximately)
