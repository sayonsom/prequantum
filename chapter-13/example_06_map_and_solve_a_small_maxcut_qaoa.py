from collections import Counter

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from scipy.optimize import minimize


node_count = 4
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]


def cut_value(bitstring):
    assignment = {node: int(bitstring[-1 - node]) for node in range(node_count)}
    return sum(assignment[left] != assignment[right] for left, right in edges)


reference_values = {
    format(integer, f"0{node_count}b"): cut_value(format(integer, f"0{node_count}b"))
    for integer in range(2**node_count)
}
reference_optimum = max(reference_values.values())
reference_solutions = sorted(
    bitstring for bitstring, value in reference_values.items() if value == reference_optimum
)


def qaoa_state(gamma, beta):
    circuit = QuantumCircuit(node_count)
    circuit.h(range(node_count))
    for left, right in edges:
        circuit.rzz(-float(gamma), left, right)
    for qubit in range(node_count):
        circuit.rx(2.0 * float(beta), qubit)
    return Statevector.from_instruction(circuit)


def expected_cut(parameters):
    probabilities = qaoa_state(parameters[0], parameters[1]).probabilities()
    return float(
        sum(
            probabilities[integer] * reference_values[format(integer, f"0{node_count}b")]
            for integer in range(2**node_count)
        )
    )


grid = np.linspace(0.0, np.pi, 17)
initial_parameters = max(
    ((gamma, beta) for gamma in grid for beta in grid),
    key=expected_cut,
)
result = minimize(
    lambda parameters: -expected_cut(parameters),
    x0=np.array(initial_parameters),
    method="L-BFGS-B",
    bounds=[(0.0, 2.0 * np.pi), (0.0, np.pi)],
    options={"ftol": 1e-12, "gtol": 1e-10, "maxiter": 500},
)

optimized_state = qaoa_state(result.x[0], result.x[1])
optimized_probabilities = optimized_state.probabilities()
rng = np.random.default_rng(211)
sampled_integers = rng.choice(2**node_count, size=2000, p=optimized_probabilities)
sample_counts = Counter(format(int(value), f"0{node_count}b") for value in sampled_integers)
best_sampled_bitstring = max(sample_counts, key=lambda label: (cut_value(label), sample_counts[label]))

assert result.success
assert reference_optimum == 4
assert cut_value(best_sampled_bitstring) == reference_optimum
assert set(reference_solutions) == {"0101", "1010"}

print("mapping=Qiskit string q3q2q1q0; node q is read from position -(q+1)")
print("cost=sum_(u,v) (1-Z_u Z_v)/2")
print(f"constant_offset={len(edges) / 2:.1f}")
print(f"optimized_gamma={result.x[0]:.6f}")
print(f"optimized_beta={result.x[1]:.6f}")
print(f"optimized_expected_cut={expected_cut(result.x):.6f}")
print(f"best_sampled_bitstring={best_sampled_bitstring}")
print(f"best_sampled_cut={cut_value(best_sampled_bitstring)}")
print(f"classical_reference_optimum={reference_optimum}")
print(f"classical_reference_solutions={reference_solutions}")
