"""Build and sample the same Bell experiment in three quantum SDKs."""

from __future__ import annotations

from collections import Counter

import cirq
import pennylane as qml
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


SHOTS = 1024
SEED = 7


def normalize(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    return {key: counts.get(key, 0) / total for key in ("00", "01", "10", "11")}


# Qiskit: a mutable QuantumCircuit followed by a Sampler primitive.
qiskit_circuit = QuantumCircuit(2)
qiskit_circuit.h(0)
qiskit_circuit.cx(0, 1)
qiskit_circuit.measure_all()
qiskit_result = StatevectorSampler(seed=SEED).run(
    [qiskit_circuit], shots=SHOTS
).result()
qiskit_counts = qiskit_result[0].data.meas.get_counts()

# Cirq: operations collected into moments and executed through a Sampler.
q0, q1 = cirq.LineQubit.range(2)
cirq_circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key="m"),
)
cirq_result = cirq.Simulator(seed=SEED).run(cirq_circuit, repetitions=SHOTS)
cirq_histogram = cirq_result.histogram(key="m")
cirq_counts = {
    format(outcome, "02b"): count for outcome, count in cirq_histogram.items()
}

# PennyLane: a quantum function bound to a device as a QNode.
pennylane_device = qml.device("default.qubit", wires=2, seed=SEED)


@qml.set_shots(shots=SHOTS)
@qml.qnode(pennylane_device)
def pennylane_circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.counts(wires=[0, 1])


pennylane_counts = Counter(
    {str(key): int(value) for key, value in pennylane_circuit().items()}
)

records = {
    "Qiskit": normalize(qiskit_counts),
    "Cirq": normalize(cirq_counts),
    "PennyLane": normalize(dict(pennylane_counts)),
}

for sdk, probabilities in records.items():
    assert probabilities["01"] == 0.0
    assert probabilities["10"] == 0.0
    print(
        f"{sdk:10s} P(00)={probabilities['00']:.3f} "
        f"P(11)={probabilities['11']:.3f}"
    )
