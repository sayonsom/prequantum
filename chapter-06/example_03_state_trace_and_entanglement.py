"""Trace a one-qubit sequence and a Bell circuit at exact checkpoints."""

import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


root_two = np.sqrt(2.0)

one_wire = QuantumCircuit(1, name="one_wire_trace")
one_wire.x(0)
one_wire.h(0)
one_wire.h(0)
one_wire.x(0)

one_wire_state = Statevector.from_instruction(one_wire)
assert one_wire_state.equiv(Statevector.from_label("0"))

after_h_circuit = QuantumCircuit(2, name="after_h")
after_h_circuit.h(0)

bell_circuit = after_h_circuit.copy(name="bell")
bell_circuit.cx(0, 1)

after_h = Statevector.from_instruction(after_h_circuit)
after_cx = Statevector.from_instruction(bell_circuit)

expected_after_h = np.array([1, 1, 0, 0], dtype=complex) / root_two
expected_after_cx = np.array([1, 0, 0, 1], dtype=complex) / root_two

assert np.allclose(after_h.data, expected_after_h)
assert np.allclose(after_cx.data, expected_after_cx)
bell_probabilities = after_cx.probabilities_dict()
assert set(bell_probabilities) == {"00", "11"}
assert np.allclose([bell_probabilities["00"], bell_probabilities["11"]], [0.5, 0.5])

recovered = after_cx.evolve(bell_circuit.inverse())
assert recovered.equiv(Statevector.from_label("00"))

print("after H on q[0]:", after_h)
print("after CX(q[0], q[1]):", after_cx)
print("ideal Z-basis support:", sorted(after_cx.probabilities_dict()))
print("recovered by inverse:", recovered.equiv(Statevector.from_label("00")))
