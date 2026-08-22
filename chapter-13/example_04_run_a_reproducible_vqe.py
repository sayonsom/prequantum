import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import minimize


hamiltonian = SparsePauliOp.from_list(
    [
        ("IZZ", -1.0),
        ("ZZI", -1.0),
        ("IIX", -0.6),
        ("IXI", -0.6),
        ("XII", -0.6),
    ]
)
exact_ground_energy = float(np.linalg.eigvalsh(hamiltonian.to_matrix())[0])
qubit_count = 3
layer_count = 2


def prepare_state(parameters):
    circuit = QuantumCircuit(qubit_count)
    cursor = 0
    for _ in range(layer_count):
        for qubit in range(qubit_count):
            circuit.ry(float(parameters[cursor]), qubit)
            cursor += 1
        circuit.cx(0, 1)
        circuit.cx(1, 2)
    return Statevector.from_instruction(circuit)


def run_vqe(seed):
    rng = np.random.default_rng(seed)
    initial_parameters = rng.uniform(-0.25, 0.25, qubit_count * layer_count)
    evaluations = 0

    def energy(parameters):
        nonlocal evaluations
        evaluations += 1
        state = prepare_state(parameters)
        return float(np.real(state.expectation_value(hamiltonian)))

    result = minimize(
        energy,
        x0=initial_parameters,
        method="COBYLA",
        options={"maxiter": 1200, "tol": 1e-10, "catol": 1e-10},
    )
    return {
        "seed": seed,
        "initial_parameters": initial_parameters,
        "final_parameters": result.x,
        "energy": float(result.fun),
        "evaluations": evaluations,
        "success": bool(result.success),
    }


first_run = run_vqe(seed=31)
repeated_run = run_vqe(seed=31)

assert np.allclose(first_run["initial_parameters"], repeated_run["initial_parameters"])
assert np.allclose(first_run["final_parameters"], repeated_run["final_parameters"])
assert np.isclose(first_run["energy"], repeated_run["energy"])
assert first_run["energy"] >= exact_ground_energy - 1e-10
assert first_run["energy"] - exact_ground_energy < 0.08

print("evidence_level=ideal_statevector")
print(f"seed={first_run['seed']}")
print("optimizer=COBYLA")
print(f"objective_evaluations={first_run['evaluations']}")
print(f"vqe_energy={first_run['energy']:.9f}")
print(f"exact_ground_energy={exact_ground_energy:.9f}")
print(f"absolute_energy_error={first_run['energy'] - exact_ground_energy:.9f}")
print("repeat_with_same_seed=True")
