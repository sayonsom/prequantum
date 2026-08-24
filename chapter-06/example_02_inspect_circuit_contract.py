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

stored_signature = []

for instruction in circuit.data:
    q_indices = [circuit.find_bit(bit).index for bit in instruction.qubits]
    c_indices = [circuit.find_bit(bit).index for bit in instruction.clbits]
    stored_signature.append((instruction.operation.name, q_indices, c_indices))
    print(instruction.operation.name, "q=", q_indices, "c=", c_indices)

default_view = circuit.draw(output="text", fold=-1)
reversed_view = circuit.draw(output="text", fold=-1, reverse_bits=True)
print("default drawing:\n", default_view)
print("reversed presentation:\n", reversed_view)

signature_after_drawing = []
for instruction in circuit.data:
    signature_after_drawing.append(
        (
            instruction.operation.name,
            [circuit.find_bit(bit).index for bit in instruction.qubits],
            [circuit.find_bit(bit).index for bit in instruction.clbits],
        )
    )

assert signature_after_drawing == stored_signature
