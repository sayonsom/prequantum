"""Use a mid-circuit result to choose a corrective operation."""

from qiskit import QuantumCircuit
from qiskit.circuit import ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator


q = QuantumRegister(1, "q")
first = ClassicalRegister(1, "first")
final = ClassicalRegister(1, "final")
circuit = QuantumCircuit(q, first, final)

circuit.h(q[0])
circuit.measure(q[0], first[0])
with circuit.if_test((first[0], 1)):
    circuit.x(q[0])
circuit.measure(q[0], final[0])

counts = AerSimulator().run(
    circuit,
    shots=64,
    seed_simulator=17,
).result().get_counts()

# With two classical registers, each key is displayed as "final first".
final_bits = {key.split()[0] for key in counts}
first_bits = {key.split()[1] for key in counts}

print("observed first-measurement branches:", sorted(first_bits))
print("observed final values:", sorted(final_bits))
print("final result is zero on both branches:", final_bits == {"0"})

assert first_bits == {"0", "1"}
assert final_bits == {"0"}
