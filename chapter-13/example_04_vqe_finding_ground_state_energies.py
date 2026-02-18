"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.3 VQE: Finding Ground State Energies
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_04_vqe_finding_ground_state_energies.py
"""

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize
import numpy as np

# Hamiltonian: H = -Z⊗Z - 0.5(X⊗I + I⊗X) + 0.3 Y⊗Y
H = SparsePauliOp.from_list([
    ('ZZ', -1.0),
    ('XI', -0.5),
    ('IX', -0.5),
    ('YY', 0.3),
])

# Exact ground state energy
H_matrix = H.to_matrix().toarray()
exact_E0 = np.linalg.eigvalsh(H_matrix)[0]
print(f"Exact ground state energy: {exact_E0:.6f}")

# Build ansatz
n_qubits = 2
n_layers = 2
n_params = n_qubits * (n_layers + 1)  # Ry on each qubit per layer + final

params = [Parameter(f'θ{i}') for i in range(n_params)]

def build_ansatz(n_qubits, n_layers, params):
    qc = QuantumCircuit(n_qubits)
    p = 0
    for layer in range(n_layers):
        # Rotation layer
        for q in range(n_qubits):
            qc.ry(params[p], q)
            p += 1
        # Entangling layer
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
    # Final rotation layer
    for q in range(n_qubits):
        qc.ry(params[p], q)
        p += 1
    return qc

ansatz = build_ansatz(n_qubits, n_layers, params)

# VQE cost function
eval_count = 0
history = []

def vqe_cost(param_values):
    global eval_count
    eval_count += 1
    bound = ansatz.assign_parameters(dict(zip(params, param_values)))
    sv = Statevector.from_instruction(bound)
    energy = sv.expectation_value(H).real
    history.append(energy)
    return energy

# Run optimizer
np.random.seed(42)
x0 = np.random.randn(n_params) * 0.1
result = minimize(vqe_cost, x0, method='COBYLA', options={'maxiter': 300})

print(f"\nVQE result:")
print(f"  Energy:          {result.fun:.6f}")
print(f"  Exact:           {exact_E0:.6f}")
print(f"  Error:           {abs(result.fun - exact_E0):.8f}")
print(f"  Iterations:      {eval_count}")

# Show convergence
checkpoints = [0, 10, 50, 100, len(history)-1]
print(f"\nConvergence:")
for i in checkpoints:
    if i < len(history):
        print(f"  Eval {i:4d}: energy = {history[i]:.6f}")
