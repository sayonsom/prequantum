"""Run one ideal Deutsch-Jozsa query and one measurement shot."""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


input_width = 4
oracle = QuantumCircuit(input_width + 1, name="balanced query")
oracle.cx(0, input_width)
oracle.cx(2, input_width)

circuit = QuantumCircuit(input_width + 1, input_width)
circuit.x(input_width)
circuit.h(range(input_width + 1))
circuit.compose(oracle, inplace=True)  # One application of the query gate.
circuit.h(range(input_width))
circuit.measure(range(input_width), range(input_width))

counts = AerSimulator().run(
    circuit, shots=1, seed_simulator=19
).result().get_counts()
observed = next(iter(counts))
verdict = "constant" if observed == "0" * input_width else "balanced"

print("counts:", counts)
print("oracle applications per shot: 1")
print("verdict:", verdict)

assert counts == {"0101": 1}
assert verdict == "balanced"
