import numpy as np
from qiskit.quantum_info import SparsePauliOp, Statevector


hamiltonian = SparsePauliOp.from_list([("Z", 1.0), ("X", 0.7)])
matrix = hamiltonian.to_matrix()
eigenvalues, eigenvectors = np.linalg.eigh(matrix)
exact_ground_energy = float(eigenvalues[0])
prepared_state = Statevector(np.ascontiguousarray(eigenvectors[:, 0]))
exact_prepared_energy = float(np.real(prepared_state.expectation_value(hamiltonian)))


def sample_pauli(expectation, shots, rng):
    probability_plus = (1.0 + expectation) / 2.0
    outcomes = rng.choice(
        np.array([1.0, -1.0]),
        size=shots,
        p=[probability_plus, 1.0 - probability_plus],
    )
    return float(np.mean(outcomes)), float(np.var(outcomes, ddof=1) / shots)


shots_per_term = 200
rng = np.random.default_rng(3)
z_exact = float(np.real(prepared_state.expectation_value(SparsePauliOp("Z"))))
x_exact = float(np.real(prepared_state.expectation_value(SparsePauliOp("X"))))
z_estimate, z_mean_variance = sample_pauli(z_exact, shots_per_term, rng)
x_estimate, x_mean_variance = sample_pauli(x_exact, shots_per_term, rng)

sampled_energy = z_estimate + 0.7 * x_estimate
standard_error = np.sqrt(z_mean_variance + 0.7**2 * x_mean_variance)

assert exact_prepared_energy >= exact_ground_energy - 1e-12
assert np.isclose(exact_prepared_energy, exact_ground_energy, atol=1e-12)
assert sampled_energy < exact_ground_energy
assert standard_error > 0.0

print(f"exact_ground_energy={exact_ground_energy:.6f}")
print(f"exact_prepared_energy={exact_prepared_energy:.6f}")
print(f"sampled_energy={sampled_energy:.6f}")
print(f"estimated_standard_error={standard_error:.6f}")
print(f"shots_per_term={shots_per_term}")
print("interpretation=the exact variational bound holds; this finite-shot estimate fluctuated below it")
