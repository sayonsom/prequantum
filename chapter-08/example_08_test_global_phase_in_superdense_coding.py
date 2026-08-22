"""Demonstrate that ZX and XZ differ only by global phase in this protocol."""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


def encoded_state(order):
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    for gate in order:
        getattr(circuit, gate)(0)
    return Statevector.from_instruction(circuit)


zx_state = encoded_state(("z", "x"))
xz_state = encoded_state(("x", "z"))

print("Vector for circuit order Z then X:", zx_state.data)
print("Vector for circuit order X then Z:", xz_state.data)
print("Equivalent up to global phase:", zx_state.equiv(xz_state))

assert not (zx_state.data == xz_state.data).all()
assert zx_state.equiv(xz_state)

simulator = AerSimulator()
for order in (("z", "x"), ("x", "z")):
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    for gate in order:
        getattr(circuit, gate)(0)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure([0, 1], [0, 1])
    counts = simulator.run(circuit, shots=256).result().get_counts()
    print(f"order={order} decoded counts={counts}")
    assert counts == {"11": 256}
