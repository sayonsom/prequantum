"""Build one Bell circuit, inspect it exactly, and sample its measurements."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


bell = QuantumCircuit(2, name="bell")
bell.h(0)
bell.cx(0, 1)

exact_state = Statevector.from_instruction(bell)
exact_probabilities = {
    str(label): float(probability)
    for label, probability in exact_state.probabilities_dict().items()
}

measured = bell.copy()
measured.measure_all()
sampler = StatevectorSampler(seed=17)
pub_result = sampler.run([(measured, None, 32)]).result()[0]
counts = pub_result.data.meas.get_counts()

print("exact probabilities:", exact_probabilities)
print("sampled outcomes:", sorted(counts))
print("total shots:", sum(counts.values()))

assert exact_state.equiv((Statevector.from_label("00") + Statevector.from_label("11")) / 2**0.5)
assert set(counts) <= {"00", "11"}
assert sum(counts.values()) == 32
