"""Read, compile, sample, decode, and validate a small energy-QAOA circuit."""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator


# This restricted teaching model selects indivisible capacity blocks.  It uses
# an exact-demand equality so that three decision qubits are enough.  It is not
# the surplus-bit inequality model from Example 18.2 and it is not continuous
# unit commitment or network-constrained dispatch.
capacity = np.array([5.0, 4.0, 3.0])
normalized_cost = np.array([6.0, 5.0, 4.0])
demand = 7.0
penalty = 10.0
energy_scale = 100.0


def decision(index: int) -> np.ndarray:
    """Return [x0, x1, x2] for Qiskit's little-endian basis index."""
    return np.array([(index >> qubit) & 1 for qubit in range(3)], dtype=int)


def raw_energy(index: int) -> float:
    x = decision(index)
    residual = float(capacity @ x - demand)
    return float(normalized_cost @ x + penalty * residual**2)


raw_energies = np.array([raw_energy(index) for index in range(8)])
scaled_energies = raw_energies / energy_scale

# Substituting x_i = (1 - z_i) / 2 gives the scaled Ising Hamiltonian
# H_C = 1.425 I + sum_i h_i Z_i + sum_ij J_ij Z_i Z_j.
# The identity term changes only global phase, so the circuit omits it.
identity_coefficient = 1.425
local_fields = np.array([0.47, 0.375, 0.28])
pair_fields = {(0, 1): 1.0, (0, 2): 0.75, (1, 2): 0.60}


def ising_energy(index: int) -> float:
    z = 1.0 - 2.0 * decision(index)
    value = identity_coefficient + float(local_fields @ z)
    value += sum(coefficient * z[left] * z[right]
                 for (left, right), coefficient in pair_fields.items())
    return value


assert np.allclose([ising_energy(index) for index in range(8)], scaled_energies)
optimal_index = int(np.argmin(raw_energies))
assert optimal_index == 6  # Displayed as q2 q1 q0 = 110; decoded x = [0, 1, 1].


def build_logical_qaoa(gamma: float, beta: float) -> QuantumCircuit:
    """Build one QAOA layer: H preparation, cost phase, then X mixer."""
    circuit = QuantumCircuit(3, name="energy_qaoa_p1")
    circuit.h(range(3))

    # RZ(theta) = exp(-i theta Z / 2), so theta = 2 gamma h_i.
    for qubit, coefficient in enumerate(local_fields):
        circuit.rz(2.0 * gamma * coefficient, qubit)

    # RZZ(theta) = exp(-i theta Z tensor Z / 2), so theta = 2 gamma J_ij.
    for (left, right), coefficient in pair_fields.items():
        circuit.rzz(2.0 * gamma * coefficient, left, right)

    # RX(2 beta) implements exp(-i beta X) on each qubit.
    circuit.rx(2.0 * beta, range(3))
    return circuit


def direct_probabilities(gamma: float, beta: float) -> np.ndarray:
    """Evaluate the same p=1 state without constructing an SDK circuit."""
    state = np.ones(8, dtype=complex) / np.sqrt(8.0)
    state *= np.exp(-1j * gamma * scaled_energies)
    for qubit in range(3):
        updated = np.empty_like(state)
        for basis_index in range(8):
            partner = basis_index ^ (1 << qubit)
            updated[basis_index] = (
                np.cos(beta) * state[basis_index]
                - 1j * np.sin(beta) * state[partner]
            )
        state = updated
    return np.abs(state) ** 2


# This finite grid is a classical outer loop.  Each point represents a fresh
# complete circuit evaluation; the grid is not a loop inside one quantum shot.
best = None
for gamma_value in np.linspace(0.0, 8.0 * np.pi, 241, endpoint=False):
    for beta_value in np.linspace(0.0, np.pi / 2.0, 121, endpoint=False):
        probabilities = direct_probabilities(gamma_value, beta_value)
        expected_energy = float(probabilities @ scaled_energies)
        if best is None or expected_energy < best[0]:
            best = (expected_energy, gamma_value, beta_value, probabilities)

expected_scaled_energy, gamma, beta, reference_probabilities = best
logical = build_logical_qaoa(gamma, beta)
logical_probabilities = np.asarray(Statevector.from_instruction(logical).probabilities())
maximum_probability_error = float(
    np.max(np.abs(logical_probabilities - reference_probabilities))
)
assert maximum_probability_error < 1e-12

# The declared target is an illustrative three-qubit line with a common
# RZ/SX/X/CX basis.  It is not a claim about a particular physical processor.
line_target = CouplingMap([(0, 1), (1, 0), (1, 2), (2, 1)])
transpile_options = {
    "basis_gates": ["rz", "sx", "x", "cx"],
    "coupling_map": line_target,
    "optimization_level": 1,
    "seed_transpiler": 18,
}
compiled_logical = transpile(logical, **transpile_options)
operator_equivalent = Operator(logical).equiv(Operator.from_circuit(compiled_logical))
assert operator_equivalent

measured = QuantumCircuit(3, 3)
measured.compose(logical, inplace=True)
measured.measure(range(3), range(3))
compiled_measured = transpile(measured, **transpile_options)

shots = 8192
counts = AerSimulator(seed_simulator=18).run(
    compiled_measured, shots=shots
).result().get_counts()
most_frequent_display = max(counts, key=counts.get)
decoded_x = np.array([int(bit) for bit in most_frequent_display[::-1]], dtype=int)
shot_frequency = counts[most_frequent_display] / shots

# The displayed string is c2 c1 c0 = x2 x1 x0.  Reverse it before using the
# domain model, which stores the decision as [x0, x1, x2].
assert most_frequent_display == "110"
assert decoded_x.tolist() == [0, 1, 1]
assert np.isclose(capacity @ decoded_x, demand)
assert np.isclose(normalized_cost @ decoded_x, 9.0)
assert abs(shot_frequency - logical_probabilities[optimal_index]) < 0.03

print(f"gamma={gamma:.9f}")
print(f"beta={beta:.9f}")
print(f"expected_raw_energy={expected_scaled_energy * energy_scale:.9f}")
print(f"ideal_probability_110={logical_probabilities[optimal_index]:.9f}")
print(f"shot_frequency_110={shot_frequency:.9f}")
print(f"most_frequent_display={most_frequent_display}")
print(f"decoded_x={decoded_x.tolist()}")
print(f"decoded_capacity={capacity @ decoded_x:.1f}")
print(f"decoded_cost={normalized_cost @ decoded_x:.1f}")
print(f"maximum_probability_error={maximum_probability_error:.1e}")
print(f"logical_operations={dict(logical.count_ops())}")
print(f"logical_depth={logical.depth()}")
print(f"compiled_operations={dict(compiled_logical.count_ops())}")
print(f"compiled_depth={compiled_logical.depth()}")
print(f"final_index_layout={compiled_logical.layout.final_index_layout()}")
print(f"ideal_operator_equivalent={operator_equivalent}")
print("network_validation=not represented by this three-bit teaching circuit")
