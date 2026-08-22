from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error


shots = 4096

circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])

ideal_counts = AerSimulator().run(
    circuit, shots=shots, seed_simulator=7
).result().get_counts()

noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.01, 1), ["h"]
)
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.04, 2), ["cx"]
)
noise_model.add_all_qubit_readout_error(
    ReadoutError([[0.97, 0.03], [0.02, 0.98]])
)

noisy_counts = AerSimulator(noise_model=noise_model).run(
    circuit, shots=shots, seed_simulator=7
).result().get_counts()

ideal_outcomes = {"00", "11"}
leakage_shots = sum(
    count for outcome, count in noisy_counts.items()
    if outcome not in ideal_outcomes
)

print("Ideal counts:", dict(sorted(ideal_counts.items())))
print("Noisy counts:", dict(sorted(noisy_counts.items())))
print(f"Unexpected-outcome rate: {leakage_shots / shots:.3f}")

assert set(ideal_counts).issubset(ideal_outcomes)
assert leakage_shots > 0
