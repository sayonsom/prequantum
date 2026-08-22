import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


terms = {"ZZ": -0.8, "XI": 0.4, "IX": -0.3, "YY": 0.2}
measurement_groups = {
    "ZZ": ["ZZ"],
    "XX": ["XI", "IX"],
    "YY": ["YY"],
}

circuit = QuantumCircuit(2)
circuit.ry(0.71, 0)
circuit.ry(-0.38, 1)
circuit.cx(0, 1)
state = Statevector.from_instruction(circuit)
hamiltonian = SparsePauliOp.from_list(list(terms.items()))
exact_energy = float(np.real(state.expectation_value(hamiltonian)))


def rotate_for_basis(input_state, basis):
    rotation = QuantumCircuit(2)
    for qubit, symbol in enumerate(reversed(basis)):
        if symbol == "X":
            rotation.h(qubit)
        elif symbol == "Y":
            rotation.sdg(qubit)
            rotation.h(qubit)
        elif symbol != "Z":
            raise ValueError(f"unsupported measurement basis: {symbol}")
    return input_state.evolve(rotation)


def term_eigenvalue(outcome, pauli_label):
    value = 1.0
    for qubit, symbol in enumerate(reversed(pauli_label)):
        if symbol != "I":
            value *= -1.0 if (outcome >> qubit) & 1 else 1.0
    return value


rng = np.random.default_rng(101)
shots_per_group = 4000
group_means = {}
group_mean_variances = {}
term_means = {}

for basis, group_terms in measurement_groups.items():
    rotated_state = rotate_for_basis(state, basis)
    outcomes = rng.choice(4, size=shots_per_group, p=rotated_state.probabilities())
    contribution_samples = np.zeros(shots_per_group)
    for pauli_label in group_terms:
        eigenvalues = np.array(
            [term_eigenvalue(int(outcome), pauli_label) for outcome in outcomes]
        )
        term_means[pauli_label] = float(np.mean(eigenvalues))
        contribution_samples += terms[pauli_label] * eigenvalues
    group_means[basis] = float(np.mean(contribution_samples))
    group_mean_variances[basis] = float(
        np.var(contribution_samples, ddof=1) / shots_per_group
    )

sampled_energy = float(sum(group_means.values()))
estimated_standard_error = float(np.sqrt(sum(group_mean_variances.values())))
interval = (
    sampled_energy - 2.0 * estimated_standard_error,
    sampled_energy + 2.0 * estimated_standard_error,
)

assert set(term_means) == set(terms)
assert abs(sampled_energy - exact_energy) < 3.0 * estimated_standard_error
assert interval[0] <= exact_energy <= interval[1]

print(f"measurement_groups={measurement_groups}")
print(f"shots_per_group={shots_per_group}")
print(f"term_estimates={term_means}")
print(f"sampled_energy={sampled_energy:.6f}")
print(f"estimated_standard_error={estimated_standard_error:.6f}")
print(f"two_standard_error_interval=({interval[0]:.6f}, {interval[1]:.6f})")
print(f"exact_statevector_energy={exact_energy:.6f}")
