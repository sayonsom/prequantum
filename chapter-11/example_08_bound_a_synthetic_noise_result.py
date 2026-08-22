"""Measure one Grover circuit under a declared synthetic noise model."""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


def target_phase_oracle(width, target):
    oracle = QuantumCircuit(width)
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            oracle.x(qubit)
    oracle.h(width - 1)
    oracle.mcx(list(range(width - 1)), width - 1)
    oracle.h(width - 1)
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            oracle.x(qubit)
    return oracle


def diffuser(width):
    circuit = QuantumCircuit(width)
    circuit.h(range(width))
    circuit.x(range(width))
    circuit.h(width - 1)
    circuit.mcx(list(range(width - 1)), width - 1)
    circuit.h(width - 1)
    circuit.x(range(width))
    circuit.h(range(width))
    return circuit


width = 3
target = "101"
iterations = 2
shots = 4000

circuit = QuantumCircuit(width, width)
circuit.h(range(width))
for _ in range(iterations):
    circuit.compose(target_phase_oracle(width, target), inplace=True)
    circuit.compose(diffuser(width), inplace=True)
circuit.measure(range(width), range(width))

noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.001, 1), ["sx", "x"])
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), "cx")
noisy_backend = AerSimulator(noise_model=noise_model)

compiled = transpile(
    circuit,
    noisy_backend,
    optimization_level=0,
    seed_transpiler=59,
)

ideal_counts = AerSimulator().run(
    compiled, shots=shots, seed_simulator=59
).result().get_counts()
noisy_counts = noisy_backend.run(
    compiled, shots=shots, seed_simulator=59
).result().get_counts()

ideal_success = ideal_counts.get(target, 0) / shots
noisy_success = noisy_counts.get(target, 0) / shots

print("declared one-qubit depolarizing rate: 0.001")
print("declared CX depolarizing rate: 0.02")
print("compiled CX count:", compiled.count_ops().get("cx", 0))
print("compiled depth:", compiled.depth())
print(f"ideal sampled success: {ideal_success:.3f}")
print(f"synthetic-noise success: {noisy_success:.3f}")

assert ideal_success > 0.92
assert 1 / 8 < noisy_success < ideal_success

# This is evidence about the declared simulator model only, not a hardware claim.
