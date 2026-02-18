"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 4: The AI Lab > Break This (Advanced)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_12_break_this_advanced.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize

# 8-vertex random graph
edges = [(0,1),(0,3),(1,2),(1,4),(2,3),(2,5),(3,6),(4,5),(4,7),(5,6),(6,7)]
n_qubits = 8

cost_terms = []
for i, j in edges:
    pauli_str = ['I'] * n_qubits
    pauli_str[i] = 'Z'
    pauli_str[j] = 'Z'
    cost_terms.append((''.join(reversed(pauli_str)), 0.5))
C_op = SparsePauliOp.from_list(cost_terms)

def qaoa_cost(params):
    gamma, beta = params  # BUG: only p=1 for a hard instance
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    for i, j in edges:
        qc.cx(i, j)
        qc.rz(gamma, j)
        qc.cx(i, j)
    for q in range(n_qubits):
        qc.rx(2 * beta, q)
    sv = Statevector.from_instruction(qc)
    zz_exp = sv.expectation_value(C_op).real
    return -(len(edges)/2 - zz_exp)

# BUG: single random init, no multi-start
result = minimize(qaoa_cost, x0=[0.5, 0.5], method='COBYLA')
print(f"QAOA expected cut: {-result.fun:.2f} out of max ~{len(edges)}")
# This will give a poor result. Fix: use p≥3 and multi-start optimization.
