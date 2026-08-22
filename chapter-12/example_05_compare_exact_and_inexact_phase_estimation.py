import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def append_inverse_qft(circuit, qubits):
    width = len(qubits)
    for left in range(width // 2):
        circuit.swap(qubits[left], qubits[width - 1 - left])
    for target in range(width):
        for control in range(target):
            angle = -np.pi / 2 ** (target - control)
            circuit.cp(angle, qubits[control], qubits[target])
        circuit.h(qubits[target])


def phase_estimation_probabilities(phase, counting_width):
    target = counting_width
    circuit = QuantumCircuit(counting_width + 1)
    circuit.h(range(counting_width))
    circuit.x(target)  # |1> is an eigenvector of the declared phase gate.
    for control in range(counting_width):
        circuit.cp(2 * np.pi * phase * 2**control, control, target)
    append_inverse_qft(circuit, list(range(counting_width)))
    state = Statevector.from_instruction(circuit)
    return {
        int(str(label), 2): float(probability)
        for label, probability in state.probabilities_dict(qargs=range(counting_width)).items()
    }


def analytic_probability(outcome, phase, counting_width):
    size = 2**counting_width
    delta = phase - outcome / size
    if np.isclose(delta, 0.0):
        return 1.0
    ratio = np.sin(np.pi * size * delta) / (size * np.sin(np.pi * delta))
    return float(ratio**2)


exact_phase = 1 / 8
exact = phase_estimation_probabilities(exact_phase, counting_width=3)
assert np.isclose(exact[1], 1.0)

inexact_phase = 1 / 3
width = 5
inexact = phase_estimation_probabilities(inexact_phase, counting_width=width)
analytic = {
    outcome: analytic_probability(outcome, inexact_phase, width)
    for outcome in range(2**width)
}
assert np.allclose(
    [inexact[y] for y in range(2**width)],
    [analytic[y] for y in range(2**width)],
)

nearest = round((2**width) * inexact_phase)
assert inexact[nearest] >= 4 / np.pi**2
top = sorted(inexact.items(), key=lambda item: -item[1])[:4]

print("exact_phase=0.125000 outcome=001 probability=1.000000")
print(f"inexact_phase={inexact_phase:.6f}")
for outcome, probability in top:
    print(f"outcome={outcome:05b} estimate={outcome/2**width:.6f} probability={probability:.6f}")
print(f"nearest_outcome_lower_bound={4/np.pi**2:.6f}")
