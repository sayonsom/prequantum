"""Contrast exact probabilities with phase-sensitive expectation values."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp, Statevector


def bell_state(relative_minus: bool) -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    if relative_minus:
        circuit.z(0)
    return circuit


phi_plus = bell_state(relative_minus=False)
phi_minus = bell_state(relative_minus=True)

plus_probabilities = {
    str(key): float(value)
    for key, value in Statevector.from_instruction(phi_plus).probabilities_dict().items()
}
minus_probabilities = {
    str(key): float(value)
    for key, value in Statevector.from_instruction(phi_minus).probabilities_dict().items()
}

observables = [SparsePauliOp("XX"), SparsePauliOp("ZZ")]
estimator = StatevectorEstimator()
plus_evs = estimator.run([(phi_plus, observables)]).result()[0].data.evs
minus_evs = estimator.run([(phi_minus, observables)]).result()[0].data.evs

print("same standard-basis probabilities:", plus_probabilities == minus_probabilities)
print("Phi-plus <XX>, <ZZ>:", plus_evs)
print("Phi-minus <XX>, <ZZ>:", minus_evs)

assert plus_probabilities == minus_probabilities
assert list(plus_evs.round(10)) == [1.0, 1.0]
assert list(minus_evs.round(10)) == [-1.0, 1.0]
