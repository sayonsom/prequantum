"""Compare sparse and dense BV circuits under one declared noise model."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def bv_circuit(secret):
    width = len(secret)
    circuit = QuantumCircuit(width + 1, width)
    circuit.x(width)
    circuit.h(range(width + 1))
    for qubit, bit in enumerate(reversed(secret)):
        if bit == "1":
            circuit.cx(qubit, width)
    circuit.h(range(width))
    circuit.measure(range(width), range(width))
    return circuit


noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.08, 2), "cx")
ideal = AerSimulator()
noisy = AerSimulator(noise_model=noise_model)

shots = 4000
success = {}
for secret in ("000001", "111111"):
    circuit = bv_circuit(secret)
    ideal_counts = ideal.run(circuit, shots=1, seed_simulator=31).result().get_counts()
    noisy_counts = noisy.run(
        circuit, shots=shots, seed_simulator=31
    ).result().get_counts()
    success[secret] = noisy_counts.get(secret, 0) / shots
    print(
        f"secret={secret} cx_count={secret.count('1')} "
        f"ideal={ideal_counts} noisy_success={success[secret]:.3f}"
    )
    assert ideal_counts == {secret: 1}

assert success["000001"] > success["111111"]

# The result supports a claim about this synthetic depolarizing model only.
# It is not a measurement or prediction of any current quantum processor.
