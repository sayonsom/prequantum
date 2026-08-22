"""Inspect a circuit through public Qiskit attributes."""

from qiskit import QuantumCircuit
from qiskit.circuit import ClassicalRegister, QuantumRegister


qubits = QuantumRegister(2, "q")
readout = ClassicalRegister(2, "readout")
circuit = QuantumCircuit(qubits, readout, name="bell_readout")
circuit.h(qubits[0])
circuit.cx(qubits[0], qubits[1])
circuit.measure(qubits, readout)

print("name:", circuit.name)
print("qubits:", circuit.num_qubits)
print("classical bits:", circuit.num_clbits)
print("operations:", circuit.size())
print("logical depth:", circuit.depth())

for instruction in circuit.data:
    q_indices = [circuit.find_bit(bit).index for bit in instruction.qubits]
    c_indices = [circuit.find_bit(bit).index for bit in instruction.clbits]
    print(instruction.operation.name, "q=", q_indices, "c=", c_indices)
