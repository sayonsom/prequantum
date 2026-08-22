"""Audit target bit order and query counts in a reusable Qiskit circuit."""

from math import asin, ceil, floor, pi, sin, sqrt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def success_probability(size, marked_count, iterations):
    theta = asin(sqrt(marked_count / size))
    return sin((2 * iterations + 1) * theta) ** 2


def best_first_peak_iteration(size, marked_count):
    theta = asin(sqrt(marked_count / size))
    continuous = pi / (4 * theta) - 0.5
    candidates = {0, max(0, floor(continuous)), max(0, ceil(continuous))}
    return max(candidates, key=lambda k: success_probability(size, marked_count, k))


def target_phase_gate(width, target):
    circuit = QuantumCircuit(width, name="MARK")
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            circuit.x(qubit)
    circuit.h(width - 1)
    circuit.mcx(list(range(width - 1)), width - 1)
    circuit.h(width - 1)
    for qubit, bit in enumerate(reversed(target)):
        if bit == "0":
            circuit.x(qubit)
    return circuit.to_gate(label="MARK")


def diffusion_gate(width):
    circuit = QuantumCircuit(width, name="DIFFUSE")
    circuit.h(range(width))
    circuit.x(range(width))
    circuit.h(width - 1)
    circuit.mcx(list(range(width - 1)), width - 1)
    circuit.h(width - 1)
    circuit.x(range(width))
    circuit.h(range(width))
    return circuit.to_gate(label="DIFFUSE")


def build_search(width, target):
    iterations = best_first_peak_iteration(2**width, 1)
    circuit = QuantumCircuit(width)
    circuit.h(range(width))
    mark = target_phase_gate(width, target)
    diffuse = diffusion_gate(width)
    for _ in range(iterations):
        circuit.append(mark, range(width))
        circuit.append(diffuse, range(width))
    return circuit, iterations


shots = 1000
for target in ("0000", "0101", "1111"):
    circuit, iterations = build_search(4, target)
    probability = Statevector.from_instruction(circuit).probabilities_dict()[target]
    mark_calls = circuit.count_ops().get("MARK", 0)
    print(
        f"target={target} k={iterations} p={probability:.6f} "
        f"queries_per_execution={mark_calls} batch_queries={mark_calls * shots}"
    )
    assert mark_calls == iterations
    assert probability > 0.95
