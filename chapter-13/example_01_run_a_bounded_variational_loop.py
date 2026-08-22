import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import minimize


hamiltonian = SparsePauliOp.from_list([("Z", -0.8), ("X", -0.6)])
exact_eigenvalues = np.linalg.eigvalsh(hamiltonian.to_matrix())
exact_ground_energy = float(exact_eigenvalues[0])


def prepare_state(theta):
    circuit = QuantumCircuit(1)
    circuit.ry(float(theta), 0)
    return Statevector.from_instruction(circuit)


def energy(theta_array):
    state = prepare_state(theta_array[0])
    return float(np.real(state.expectation_value(hamiltonian)))


result = minimize(
    energy,
    x0=np.array([0.25]),
    method="L-BFGS-B",
    bounds=[(-np.pi, np.pi)],
    options={"ftol": 1e-12, "gtol": 1e-10, "maxiter": 200},
)
optimized_energy = energy(result.x)

problem_record = {
    "operator": "-0.8 Z - 0.6 X",
    "reference": "exact matrix diagonalization",
}
state_family_record = {
    "initial_state": "|0>",
    "ansatz": "Ry(theta)|0>",
    "parameter_domain": "[-pi, pi]",
}
evaluation_record = {
    "estimator": "exact statevector expectation",
    "optimizer": "bounded L-BFGS-B",
    "initial_theta": 0.25,
}
evidence_record = {
    "level": "ideal_statevector",
    "supports": "this one-qubit model and declared state family",
}

assert result.success
assert optimized_energy >= exact_ground_energy - 1e-10
assert np.isclose(optimized_energy, exact_ground_energy, atol=1e-9)

print(f"problem_record={problem_record}")
print(f"state_family_record={state_family_record}")
print(f"evaluation_record={evaluation_record}")
print(f"evidence_record={evidence_record}")
print(f"optimized_theta={result.x[0]:.9f}")
print(f"optimized_energy={optimized_energy:.9f}")
print(f"exact_ground_energy={exact_ground_energy:.9f}")
