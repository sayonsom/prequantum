"""Run a bounded Grover experiment with explicit query and shot counts."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def target_phase_oracle(width, target):
    oracle = QuantumCircuit(width, name="MARK")
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
    circuit = QuantumCircuit(width, name="DIFFUSE")
    circuit.h(range(width))
    circuit.x(range(width))
    circuit.h(width - 1)
    circuit.mcx(list(range(width - 1)), width - 1)
    circuit.h(width - 1)
    circuit.x(range(width))
    circuit.h(range(width))
    return circuit


width = 3
target = "101"  # Display order is q2 q1 q0.
iterations = 2
shots = 2048

circuit = QuantumCircuit(width, width)
circuit.h(range(width))
for _ in range(iterations):
    circuit.compose(target_phase_oracle(width, target), inplace=True)
    circuit.compose(diffuser(width), inplace=True)
circuit.measure(range(width), range(width))

counts = AerSimulator().run(
    circuit, shots=shots, seed_simulator=41
).result().get_counts()
success = counts.get(target, 0) / shots

print("target:", target)
print("Grover iterations per execution:", iterations)
print("oracle applications across batch:", iterations * shots)
print(f"sampled success: {success:.3f}")

assert success > 0.90
