"""Show that Bob's local state is maximally mixed before correction data arrives."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace


def bob_state_before_message(theta, phi):
    circuit = QuantumCircuit(3)
    circuit.ry(theta, 0)
    circuit.rz(phi, 0)
    circuit.h(1)
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.h(0)
    joint_state = Statevector.from_instruction(circuit)
    return partial_trace(joint_state, [0, 1]).data


maximally_mixed = np.eye(2, dtype=complex) / 2

for theta, phi in [(0.0, 0.0), (np.pi, 0.0), (np.pi / 2, 0.0), (1.1, 0.7)]:
    bob = bob_state_before_message(theta, phi)
    print(f"theta={theta:.3f} phi={phi:.3f}\n{np.round(bob, 6)}")
    assert np.allclose(bob, maximally_mixed)
