"""Recover a Bernstein-Vazirani secret with an explicit bit-order contract."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# Semantic string order is s_(n-1) ... s_0, matching Qiskit's displayed count key.
secret = "10110"
width = len(secret)
oracle = QuantumCircuit(width + 1, name="BV query")
for qubit, bit in enumerate(reversed(secret)):
    if bit == "1":
        oracle.cx(qubit, width)

circuit = QuantumCircuit(width + 1, width)
circuit.x(width)
circuit.h(range(width + 1))
circuit.compose(oracle, inplace=True)  # One query application.
circuit.h(range(width))
circuit.measure(range(width), range(width))

counts = AerSimulator().run(
    circuit, shots=1, seed_simulator=23
).result().get_counts()
displayed = next(iter(counts))

print("semantic secret:", secret)
print("displayed count: ", displayed)
print("qubit-to-secret mapping:", list(enumerate(reversed(secret))))

assert counts == {secret: 1}
