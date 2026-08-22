import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


shots = 50_000
base_error = 0.02
noise_factors = np.array([1.0, 2.0, 3.0])
expectations = []

circuit = QuantumCircuit(1, 1)
circuit.h(0)
circuit.h(0)
circuit.measure(0, 0)

for factor in noise_factors:
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(base_error * factor, 1), ["h"]
    )
    counts = AerSimulator(noise_model=noise_model).run(
        circuit, shots=shots, seed_simulator=23
    ).result().get_counts()
    expectation_z = (
        counts.get("0", 0) - counts.get("1", 0)
    ) / shots
    expectations.append(expectation_z)

expectations = np.array(expectations)
line = np.polyfit(noise_factors, expectations, deg=1)
zero_noise_estimate = np.polyval(line, 0.0)

for factor, value in zip(noise_factors, expectations):
    print(f"noise factor {factor:.0f}: <Z> = {value:.4f}")
print(f"linear zero-noise estimate: {zero_noise_estimate:.4f}")
print("ideal value: 1.0000")

assert abs(zero_noise_estimate - 1.0) < abs(expectations[0] - 1.0)
