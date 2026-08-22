from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

circuit = QuantumCircuit(1, 1)
circuit.h(0)
circuit.h(0)
circuit.measure(0, 0)

simulator = AerSimulator()
result = simulator.run(
    circuit,
    shots=1000,
    seed_simulator=42,
).result()

print(result.get_counts())
# {'0': 1000}
