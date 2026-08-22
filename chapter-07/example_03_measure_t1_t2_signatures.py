import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error


t1 = 200e-6
t2 = 120e-6
shots = 20_000
wait_times = [0.0, 40e-6, 120e-6, 240e-6]

assert 0 < t2 <= 2 * t1

print("wait_us  T1:P(1) empirical/theory  T2:P(+) empirical/theory")

for wait_time in wait_times:
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        thermal_relaxation_error(t1, t2, wait_time), ["id"]
    )
    simulator = AerSimulator(noise_model=noise_model)

    t1_circuit = QuantumCircuit(1, 1)
    t1_circuit.x(0)
    t1_circuit.id(0)
    t1_circuit.measure(0, 0)

    t2_circuit = QuantumCircuit(1, 1)
    t2_circuit.h(0)
    t2_circuit.id(0)
    t2_circuit.h(0)
    t2_circuit.measure(0, 0)

    t1_counts = simulator.run(
        t1_circuit, shots=shots, seed_simulator=11
    ).result().get_counts()
    t2_counts = simulator.run(
        t2_circuit, shots=shots, seed_simulator=13
    ).result().get_counts()

    empirical_t1 = t1_counts.get("1", 0) / shots
    empirical_t2 = t2_counts.get("0", 0) / shots
    theory_t1 = np.exp(-wait_time / t1)
    theory_t2 = 0.5 * (1 + np.exp(-wait_time / t2))

    print(
        f"{wait_time * 1e6:7.1f}  "
        f"{empirical_t1:.3f}/{theory_t1:.3f}             "
        f"{empirical_t2:.3f}/{theory_t2:.3f}"
    )
