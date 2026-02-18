"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.8 Barren Plateaus: The Scalability Wall
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_09_barren_plateaus_the_scalability_wall.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

def random_ansatz(n_qubits, n_layers):
    """Build a random hardware-efficient ansatz."""
    qc = QuantumCircuit(n_qubits)
    params = []
    for layer in range(n_layers):
        angles = np.random.uniform(0, 2*np.pi, n_qubits)
        for q in range(n_qubits):
            qc.ry(angles[q], q)
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
        params.extend(angles)
    return qc, params

# Measure gradient variance as system size increases
print("Barren plateau demonstration:")
print(f"{'n_qubits':>10s} {'n_layers':>10s} {'grad_variance':>15s} {'shots_needed':>15s}")
print("-" * 55)

for n_qubits in [2, 4, 6, 8, 10]:
    n_layers = n_qubits  # depth scales with width

    # Observable: Z on first qubit
    pauli_str = 'I' * (n_qubits - 1) + 'Z'
    obs = SparsePauliOp.from_list([(pauli_str, 1.0)])

    gradients = []
    for _ in range(200):
        qc, _ = random_ansatz(n_qubits, n_layers)
        sv = Statevector.from_instruction(qc)
        exp_val = sv.expectation_value(obs).real
        gradients.append(exp_val)

    var = np.var(gradients)
    # To detect a gradient of magnitude √var with confidence,
    # you need O(1/var) shots
    shots_needed = int(1.0 / max(var, 1e-10))
    print(f"{n_qubits:10d} {n_layers:10d} {var:15.6f} {shots_needed:>15,d}")

print("\nVariance shrinks exponentially → gradients vanish → optimization stalls")
print("This is why 'just add more qubits' doesn't work for random variational circuits.")
