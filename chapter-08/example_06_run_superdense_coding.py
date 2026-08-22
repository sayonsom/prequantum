"""Send a pair of classical bits with one transmitted qubit and one shared ebit."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def superdense_circuit(phase_bit, flip_bit):
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)  # Alice holds q0; Bob holds q1.

    if phase_bit:
        circuit.z(0)
    if flip_bit:
        circuit.x(0)

    # Alice now transmits q0. Bob decodes both qubits.
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)  # c0 recovers the phase bit.
    circuit.measure(1, 1)  # c1 recovers the flip bit.
    return circuit


simulator = AerSimulator()

for phase_bit in (0, 1):
    for flip_bit in (0, 1):
        circuit = superdense_circuit(phase_bit, flip_bit)
        counts = simulator.run(
            circuit, shots=256, seed_simulator=31
        ).result().get_counts()
        displayed = max(counts, key=counts.get)  # Qiskit displays c1 then c0.
        decoded_phase = int(displayed[1])
        decoded_flip = int(displayed[0])
        decoded = (decoded_phase, decoded_flip)
        sent = (phase_bit, flip_bit)
        print(f"sent={sent} displayed={displayed} decoded={decoded}")
        assert decoded == sent
