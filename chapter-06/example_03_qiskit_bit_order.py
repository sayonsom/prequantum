"""Make Qiskit's qubit, ket-label, and displayed-count ordering explicit."""

from qiskit import QuantumCircuit
from qiskit.circuit import ClassicalRegister, QuantumRegister
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


q = QuantumRegister(2, "q")
readout = ClassicalRegister(2, "readout")

prepare = QuantumCircuit(q)
prepare.x(q[0])
state = Statevector.from_instruction(prepare)
probabilities = {
    str(label): float(probability)
    for label, probability in state.probabilities_dict().items()
}

measure = QuantumCircuit(q, readout)
measure.compose(prepare, qubits=q, inplace=True)
measure.measure(q, readout)
counts = (
    StatevectorSampler(seed=17)
    .run([(measure, None, 8)])
    .result()[0]
    .data.readout.get_counts()
)

print("statevector index 1:", state.data[1])
print("ket-label probabilities:", probabilities)
print("displayed counts:", counts)
print("q[0] is the rightmost displayed bit:", set(counts) == {"01"})
