"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.2 Parameterized Circuits and Ansatz Design
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_03_parameterized_circuits_and_ansatz_design.py
"""

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector, SparsePauliOp
import numpy as np

# Build a parameterized ansatz
theta = [Parameter(f'θ{i}') for i in range(4)]

ansatz = QuantumCircuit(2)
# Layer 1: single-qubit rotations
ansatz.ry(theta[0], 0)
ansatz.ry(theta[1], 1)
# Entangling layer
ansatz.cx(0, 1)
# Layer 2: single-qubit rotations
ansatz.ry(theta[2], 0)
ansatz.ry(theta[3], 1)

print("Parameterized ansatz:")
print(ansatz.draw())

# Bind parameters to specific values
bound = ansatz.assign_parameters({theta[i]: 0.5 * (i + 1) for i in range(4)})
sv = Statevector.from_instruction(bound)
print(f"\nState with θ=[0.5, 1.0, 1.5, 2.0]:")
print(f"  {np.round(sv.data, 4)}")
print(f"  Probabilities: {np.round(sv.probabilities(), 4)}")

# Define a Hamiltonian using SparsePauliOp (the standard in Qiskit 1.x+)
# Note: Qiskit 2.x removed Opflow entirely. SparsePauliOp is now the
# only supported operator format.
H = SparsePauliOp.from_list([
    ('ZZ', -1.0),    # -Z⊗Z
    ('XI', -0.5),    # -0.5 * X⊗I
    ('IX', -0.5),    # -0.5 * I⊗X
])
print(f"\nHamiltonian H = {H}")
print(f"H as matrix:\n{np.round(H.to_matrix().real, 4)}")

# Compute expectation value for bound circuit
exp_val = sv.expectation_value(H).real
print(f"\n⟨ψ(θ)|H|ψ(θ)⟩ = {exp_val:.6f}")

# Compare to exact ground state
eigenvalues = np.linalg.eigvalsh(H.to_matrix().toarray())
print(f"Exact ground state energy: {eigenvalues[0]:.6f}")
