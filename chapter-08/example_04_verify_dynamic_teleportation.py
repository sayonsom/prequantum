"""Verify teleportation with mid-circuit measurement and classical feedforward."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def teleportation_verification_circuit(theta, phi):
    preparation = QuantumCircuit(1)
    preparation.ry(theta, 0)
    preparation.rz(phi, 0)

    circuit = QuantumCircuit(3, 3)
    circuit.compose(preparation, qubits=[0], inplace=True)

    circuit.h(1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)

    with circuit.if_test((circuit.clbits[1], 1)):
        circuit.x(2)
    with circuit.if_test((circuit.clbits[0], 1)):
        circuit.z(2)

    # A full-state check: the inverse preparation maps the target state to |0>.
    circuit.compose(preparation.inverse(), qubits=[2], inplace=True)
    circuit.measure(2, 2)
    return circuit


simulator = AerSimulator()
states = [(0.0, 0.0), (np.pi, 0.0), (np.pi / 2, 0.0), (1.1, 0.7)]

for theta, phi in states:
    circuit = teleportation_verification_circuit(theta, phi)
    counts = simulator.run(
        circuit, shots=1024, seed_simulator=23
    ).result().get_counts()
    bob_one = sum(count for bits, count in counts.items() if bits[0] == "1")
    print(f"theta={theta:.3f} phi={phi:.3f} Bob verification failures={bob_one}")
    assert bob_one == 0
