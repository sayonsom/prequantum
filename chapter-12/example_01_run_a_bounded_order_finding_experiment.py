from fractions import Fraction
from math import gcd, lcm

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector


def modular_multiplication_matrix(base, modulus, width):
    """Return |y> -> |base*y mod modulus> on y < modulus.

    Labels outside the arithmetic domain are fixed so that the full matrix is
    a permutation on every computational-basis label.
    """
    size = 2**width
    matrix = np.zeros((size, size), dtype=complex)
    for y in range(size):
        mapped = (base * y) % modulus if y < modulus else y
        matrix[mapped, y] = 1.0
    return matrix


def append_inverse_qft(circuit, qubits):
    """Append an inverse QFT compatible with Qiskit's displayed bit order."""
    width = len(qubits)
    for left in range(width // 2):
        circuit.swap(qubits[left], qubits[width - 1 - left])
    for target in range(width):
        for control in range(target):
            angle = -np.pi / 2 ** (target - control)
            circuit.cp(angle, qubits[control], qubits[target])
        circuit.h(qubits[target])


modulus = 15
base = 2
counting_width = 4
target_width = 4

assert gcd(base, modulus) == 1
multiplier = modular_multiplication_matrix(base, modulus, target_width)
assert np.allclose(multiplier.conj().T @ multiplier, np.eye(2**target_width))

circuit = QuantumCircuit(counting_width + target_width)
circuit.h(range(counting_width))
circuit.x(counting_width)  # The target register now holds the integer 1.

target_qubits = list(range(counting_width, counting_width + target_width))
for control in range(counting_width):
    power = 2**control
    powered_multiplier = np.linalg.matrix_power(multiplier, power)
    controlled_gate = UnitaryGate(powered_multiplier, label=f"M^{power}").control()
    circuit.append(controlled_gate, [control, *target_qubits])

append_inverse_qft(circuit, list(range(counting_width)))
state = Statevector.from_instruction(circuit)
phase_probabilities = {
    str(label): float(probability)
    for label, probability in state.probabilities_dict(qargs=range(counting_width)).items()
    if probability > 1e-10
}

denominators = []
for label in phase_probabilities:
    numerator = int(label, 2)
    if numerator == 0:
        continue
    fraction = Fraction(numerator, 2**counting_width).limit_denominator(modulus)
    denominators.append(fraction.denominator)

recovered_order = lcm(*denominators)
assert pow(base, recovered_order, modulus) == 1

half_power = pow(base, recovered_order // 2, modulus)
factors = tuple(sorted((gcd(half_power - 1, modulus), gcd(half_power + 1, modulus))))

expected_labels = {"0000", "0100", "1000", "1100"}
assert set(phase_probabilities) == expected_labels
assert all(np.isclose(probability, 0.25) for probability in phase_probabilities.values())
assert recovered_order == 4
assert factors == (3, 5)

print("evidence_level=ideal_statevector")
print(f"phase_probabilities={phase_probabilities}")
print(f"recovered_order={recovered_order}")
print(f"factors={factors}")
