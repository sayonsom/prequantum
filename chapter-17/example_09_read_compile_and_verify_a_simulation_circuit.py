"""Read, compile, and verify a complete product-formula simulation circuit."""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit.transpiler import CouplingMap
from scipy.linalg import expm


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Qiskit displays a two-qubit result as q1q0. The matching matrix basis is
# |00>, |01>, |10>, |11>, with q1 as the left bit and q0 as the right bit.
hamiltonian = np.kron(Z, Z) + 0.7 * (
    np.kron(X, I) + np.kron(I, X)
)
magnetization = 0.5 * (np.kron(Z, I) + np.kron(I, Z))
total_time = 0.8
repetitions = 2


def build_symmetric_formula(time: float, steps: int) -> QuantumCircuit:
    """Build two symmetric second-order product-formula repetitions."""
    if steps < 1:
        raise ValueError("steps must be positive")
    delta = time / steps
    circuit = QuantumCircuit(2, name="symmetric_product_formula")
    for _ in range(steps):
        # A half-step is exp(-i delta ZZ / 2). Because
        # RZZ(phi)=exp(-i phi ZZ/2), its gate angle is phi=delta.
        circuit.rzz(delta, 0, 1)

        # B=0.7*(XI+IX). The two terms commute. RX(phi) implements
        # exp(-i phi X/2), so a full B step uses phi=2*0.7*delta.
        circuit.rx(1.4 * delta, 0)
        circuit.rx(1.4 * delta, 1)

        circuit.rzz(delta, 0, 1)
    return circuit


logical = build_symmetric_formula(total_time, repetitions)
logical_operator = np.asarray(Operator(logical).data)
exact_operator = expm(-1j * hamiltonian * total_time)
product_formula_operator_error = float(
    np.linalg.norm(logical_operator - exact_operator, ord=2)
)

initial_state = Statevector.from_label("00")
logical_state = initial_state.evolve(logical)
exact_state = exact_operator @ np.asarray(initial_state.data)
logical_probabilities = np.asarray(logical_state.probabilities())
exact_probabilities = np.abs(exact_state) ** 2
maximum_probability_error = float(
    np.max(np.abs(logical_probabilities - exact_probabilities))
)

logical_magnetization = float(
    np.vdot(logical_state.data, magnetization @ logical_state.data).real
)
exact_magnetization = float(
    np.vdot(exact_state, magnetization @ exact_state).real
)

# Shots repeat the completed circuit; they are not extra coherent formula
# steps. Each array index is the integer represented by the displayed q1q0.
outcome_magnetization = np.array([1.0, 0.0, 0.0, -1.0])
rng = np.random.default_rng(1709)
shots = 4_000
samples = rng.choice(4, size=shots, p=logical_probabilities)
shot_values = outcome_magnetization[samples]
shot_estimate = float(shot_values.mean())
shot_standard_error = float(shot_values.std(ddof=1) / np.sqrt(shots))

# This declared target is a bidirectional two-qubit link with an RZ/SX/X/CX
# basis. It is a compilation fixture, not a claim about a physical processor.
line_target = CouplingMap([(0, 1), (1, 0)])
compiled = transpile(
    logical,
    basis_gates=["rz", "sx", "x", "cx"],
    coupling_map=line_target,
    optimization_level=1,
    seed_transpiler=17,
)

# Operator.from_circuit applies the transpiler layout metadata. Equivalence is
# ideal and up to global phase; it does not test device fidelity or noise.
ideal_operator_equivalent = Operator(logical).equiv(
    Operator.from_circuit(compiled)
)

assert product_formula_operator_error < 0.07
assert maximum_probability_error < 0.025
assert abs(logical_magnetization - exact_magnetization) < 0.025
assert abs(shot_estimate - logical_magnetization) <= 3 * shot_standard_error
assert ideal_operator_equivalent

print(f"delta={total_time/repetitions:.6f}")
print(f"product_formula_operator_error={product_formula_operator_error:.9f}")
print(f"maximum_probability_error={maximum_probability_error:.9f}")
print(f"exact_magnetization={exact_magnetization:.9f}")
print(f"logical_magnetization={logical_magnetization:.9f}")
print(f"shot_estimate={shot_estimate:.9f}")
print(f"shot_standard_error={shot_standard_error:.9f}")
print(f"logical_operations={dict(logical.count_ops())}")
print(f"logical_depth={logical.depth()}")
print(f"compiled_operations={dict(compiled.count_ops())}")
print(f"compiled_depth={compiled.depth()}")
print(f"final_index_layout={compiled.layout.final_index_layout()}")
print(f"ideal_operator_equivalent={ideal_operator_equivalent}")
