import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import differential_evolution


hamiltonian = SparsePauliOp.from_list([("XX", -1.0), ("ZZ", -1.0)])
exact_ground_energy = float(np.linalg.eigvalsh(hamiltonian.to_matrix())[0])


def product_state(parameters):
    circuit = QuantumCircuit(2)
    circuit.ry(float(parameters[0]), 0)
    circuit.ry(float(parameters[1]), 1)
    return Statevector.from_instruction(circuit)


def entangling_state(parameters):
    circuit = QuantumCircuit(2)
    circuit.ry(float(parameters[0]), 0)
    circuit.ry(float(parameters[1]), 1)
    circuit.cx(0, 1)
    return Statevector.from_instruction(circuit)


def minimize_family(state_function):
    def objective(parameters):
        state = state_function(parameters)
        return float(np.real(state.expectation_value(hamiltonian)))

    return differential_evolution(
        objective,
        bounds=[(-np.pi, np.pi), (-np.pi, np.pi)],
        seed=19,
        polish=True,
        tol=1e-10,
    )


def concurrence(state):
    a00, a01, a10, a11 = state.data
    return float(2.0 * abs(a00 * a11 - a01 * a10))


product_result = minimize_family(product_state)
entangling_result = minimize_family(entangling_state)
best_entangling_state = entangling_state(entangling_result.x)

assert np.isclose(product_result.fun, -1.0, atol=1e-8)
assert np.isclose(entangling_result.fun, exact_ground_energy, atol=1e-8)
assert concurrence(best_entangling_state) > 1.0 - 1e-8

print(f"exact_ground_energy={exact_ground_energy:.6f}")
print(f"best_product_family_energy={product_result.fun:.6f}")
print(f"best_entangling_family_energy={entangling_result.fun:.6f}")
print(f"best_entangling_state_concurrence={concurrence(best_entangling_state):.6f}")
print("interpretation=the optimizer cannot reach a state that the declared family excludes")
