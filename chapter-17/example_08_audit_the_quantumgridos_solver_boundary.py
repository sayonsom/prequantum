"""Record what the reviewed QuantumGridOS HHL-fast path actually returns."""

import numpy as np
from quantumgridos.algorithms.quantum_solvers import QuantumLinearSolver

# This example targets QuantumGridOS commit
# dff26bed704886e384c5f7df833828c965a7000a (package version 0.1.9).
A = np.array([[2.0, 0.25], [0.25, 1.5]])
b = np.array([1.0, -0.5])

solver = QuantumLinearSolver()
solution, proof_of_concept_circuit = solver.solve(A, b, method="hhl_fast")
classical_reference = np.linalg.solve(A, b)

print("solution:", np.round(solution, 6))
print("matches np.linalg.solve:", np.allclose(solution, classical_reference))
print("circuit returned:", proof_of_concept_circuit is not None)
print("circuit qubits:", proof_of_concept_circuit.num_qubits)
print("evidence class: classical solution plus proof-of-concept circuit")

assert np.allclose(solution, classical_reference)
assert proof_of_concept_circuit is not None
