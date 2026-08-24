"""Read, compile, and verify the p=1 QAOA circuit from Example 16.5."""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit.transpiler import CouplingMap


# The displayed bit string is ABC = q2 q1 q0. Qubit 0 is the least-significant
# bit in Qiskit strings, so variable A lives on q2 and variable C lives on q0.
variable_qubit = {"A": 2, "B": 1, "C": 0}
raw_cost = np.array([90.0, 8.0, 14.0, 52.0, 43.0, 21.0, 7.0, 105.0])
cost_range = float(raw_cost.max() - raw_cost.min())

# Raw Ising coefficients from Example 16.4, divided by the same range used in
# Example 16.5. The shifted identity coefficient is omitted because it changes
# only the global phase of the ideal circuit.
local_fields = {"A": -1.5 / cost_range, "B": -2.0 / cost_range, "C": -4.0 / cost_range}
pair_fields = {
    ("A", "B"): 10.0 / cost_range,
    ("A", "C"): 15.0 / cost_range,
    ("B", "C"): 30.0 / cost_range,
}

# These are the exact grid coordinates reported by Example 16.5.
gamma = 2.0 * np.pi * 50.0 / 181.0
beta = (np.pi / 2.0) * 94.0 / 120.0


def build_logical_qaoa(gamma_value: float, beta_value: float) -> QuantumCircuit:
    """Build H preparation, one cost layer, and one X-mixer layer."""
    circuit = QuantumCircuit(3, name="p1_qaoa")
    circuit.h(range(3))

    # RZ(theta) = exp(-i theta Z / 2), so theta = 2 gamma h_i.
    for variable, coefficient in local_fields.items():
        circuit.rz(2.0 * gamma_value * coefficient, variable_qubit[variable])

    # RZZ(theta) = exp(-i theta Z tensor Z / 2), so theta = 2 gamma J_ij.
    for (left, right), coefficient in pair_fields.items():
        circuit.rzz(
            2.0 * gamma_value * coefficient,
            variable_qubit[left],
            variable_qubit[right],
        )

    # RX(2 beta) implements exp(-i beta X) on each qubit.
    circuit.rx(2.0 * beta_value, range(3))
    return circuit


def manuscript_reference(gamma_value: float, beta_value: float) -> np.ndarray:
    """Repeat the direct state-vector calculation used in Example 16.5."""
    scaled_cost = (raw_cost - raw_cost.min()) / cost_range
    state = np.ones(8, dtype=complex) / np.sqrt(8.0)
    state *= np.exp(-1j * gamma_value * scaled_cost)
    for qubit in range(3):
        updated = np.empty_like(state)
        for basis_index in range(8):
            partner = basis_index ^ (1 << qubit)
            updated[basis_index] = (
                np.cos(beta_value) * state[basis_index]
                - 1j * np.sin(beta_value) * state[partner]
            )
        state = updated
    return np.abs(state) ** 2


logical = build_logical_qaoa(gamma, beta)
logical_probabilities = np.asarray(Statevector.from_instruction(logical).probabilities())
reference_probabilities = manuscript_reference(gamma, beta)

maximum_probability_error = float(
    np.max(np.abs(logical_probabilities - reference_probabilities))
)
expected_raw_cost = float(logical_probabilities @ raw_cost)
optimal_probability = float(logical_probabilities[int("110", 2)])

assert maximum_probability_error < 1e-12
assert np.isclose(expected_raw_cost, 17.952381, atol=1e-6)
assert np.isclose(optimal_probability, 0.247209, atol=1e-6)

# This illustrative target has a three-qubit line, a symmetric directed
# coupling map, and an RZ/SX/X/CX basis. It is a declared compilation target,
# not a claim about a particular physical processor.
line_target = CouplingMap([(0, 1), (1, 0), (1, 2), (2, 1)])
compiled = transpile(
    logical,
    basis_gates=["rz", "sx", "x", "cx"],
    coupling_map=line_target,
    optimization_level=1,
    seed_transpiler=17,
)

# Operator.from_circuit applies the transpiler layout metadata. Equivalence is
# checked up to global phase; it does not test hardware noise or fidelity.
operator_equivalent = Operator(logical).equiv(Operator.from_circuit(compiled))
assert operator_equivalent

print(f"gamma={gamma:.6f}")
print(f"beta={beta:.6f}")
print(f"expected_raw_cost={expected_raw_cost:.9f}")
print(f"probability_110={optimal_probability:.9f}")
print(f"maximum_probability_error={maximum_probability_error:.1e}")
print(f"logical_operations={dict(logical.count_ops())}")
print(f"logical_depth={logical.depth()}")
print(f"compiled_operations={dict(compiled.count_ops())}")
print(f"compiled_depth={compiled.depth()}")
print(f"final_index_layout={compiled.layout.final_index_layout()}")
print(f"ideal_operator_equivalent={operator_equivalent}")
