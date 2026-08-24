"""Synthesize a declared Pauli Hamiltonian as a readable product-formula circuit."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Operator, SparsePauliOp
from qiskit.synthesis import LieTrotter
from scipy.linalg import expm


# Qiskit Pauli labels are written q1 q0 for this two-qubit example.
hamiltonian = SparsePauliOp.from_list(
    [
        ("ZZ", -1.0),
        ("XI", -0.5),
        ("IX", -0.5),
    ]
)
total_time = 1.0


def manual_first_order(steps: int) -> QuantumCircuit:
    """Build temporal order -ZZ, -0.5 XI, -0.5 IX for every step."""
    if steps < 1:
        raise ValueError("steps must be positive")
    dt = total_time / steps
    circuit = QuantumCircuit(2)
    for _ in range(steps):
        # exp(+i ZZ dt) = RZZ(-2 dt)
        circuit.rzz(-2.0 * dt, 0, 1)
        # XI acts on q1 and IX acts on q0 in Qiskit's label order.
        circuit.rx(-dt, 1)
        circuit.rx(-dt, 0)
    return circuit


exact = expm(-1j * hamiltonian.to_matrix() * total_time)
step_counts = [1, 2, 4, 8, 16]
errors = []
for steps in step_counts:
    approximate = Operator(manual_first_order(steps)).data
    errors.append(float(np.linalg.norm(approximate - exact, ord=2)))

chosen_steps = 8
logical = QuantumCircuit(2)
logical.append(
    PauliEvolutionGate(
        hamiltonian,
        time=total_time,
        synthesis=LieTrotter(reps=chosen_steps, preserve_order=True),
    ),
    [0, 1],
)
manual = manual_first_order(chosen_steps)
synthesized = logical.decompose()

assert np.allclose(hamiltonian.to_matrix(), hamiltonian.to_matrix().conj().T)
assert np.all(np.diff(errors) < 0)
assert np.allclose(Operator(synthesized).data, Operator(manual).data, atol=1e-12)
assert np.allclose(Operator(manual).data.conj().T @ Operator(manual).data, np.eye(4))

print(f"pauli_terms={hamiltonian.to_list()}")
print(f"temporal_order=-ZZ then -0.5 XI then -0.5 IX")
print(f"manual_operations={manual.count_ops()}")
print(f"synthesized_operations={synthesized.count_ops()}")
print("steps operator_2_norm_error")
for steps, error in zip(step_counts, errors):
    print(f"{steps:5d} {error:.10f}")
print("boundary=logical synthesis and ideal operator checks do not establish target cost or hardware accuracy")
