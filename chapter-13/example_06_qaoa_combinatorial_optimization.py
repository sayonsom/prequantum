"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.5 QAOA: Combinatorial Optimization
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_06_qaoa_combinatorial_optimization.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
from scipy.optimize import minimize
import numpy as np

# --- MaxCut problem ---
# Graph: 4 vertices, 4 edges
# Edges: (0,1), (1,2), (2,3), (0,3) -- a cycle
edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
n_qubits = 4

# Cost Hamiltonian: C = Σ_{(i,j)} (1 - Z_i Z_j) / 2
# Maximizing cut ↔ minimizing -C ↔ minimizing Σ Z_i Z_j (up to constant)
cost_terms = []
for i, j in edges:
    # (1 - ZiZj)/2 per edge → we minimize the negative
    pauli_str = ['I'] * n_qubits
    pauli_str[i] = 'Z'
    pauli_str[j] = 'Z'
    cost_terms.append((''.join(reversed(pauli_str)), 0.5))  # ZZ coefficient
    # The constant (1/2 per edge) shifts the energy but doesn't affect optimization

C_op = SparsePauliOp.from_list(cost_terms)

# Classical brute force: check all 2^n partitions
print("All cuts (brute force):")
best_cut = 0
best_partition = ""
for bits in range(2**n_qubits):
    partition = format(bits, f'0{n_qubits}b')
    cut = sum(1 for i, j in edges if partition[i] != partition[j])
    if cut >= best_cut:
        best_cut = cut
        best_partition = partition
    if cut >= 3:
        print(f"  {partition}: cut = {cut}" + (" ← MAX" if cut == best_cut else ""))
print(f"Best: {best_partition} with cut = {best_cut}\n")

# --- QAOA circuit ---
def qaoa_circuit(gammas, betas, edges, n_qubits):
    """Build a p-layer QAOA circuit.

    p = len(gammas) = len(betas) is the circuit depth.
    Higher p → better approximation ratio, but deeper circuit.
    """
    qc = QuantumCircuit(n_qubits)
    p = len(gammas)

    # Initial superposition: equal weight over all partitions
    qc.h(range(n_qubits))

    for layer in range(p):
        # Cost layer: e^(-iγC) = product of e^(-iγ ZiZj/2) for each edge
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(gammas[layer], j)
            qc.cx(i, j)

        # Mixer layer: e^(-iβB) where B = Σ Xi
        for q in range(n_qubits):
            qc.rx(2 * betas[layer], q)

    return qc

# QAOA cost function
def qaoa_cost(params):
    p = len(params) // 2
    gammas = params[:p]
    betas = params[p:]
    qc = qaoa_circuit(gammas, betas, edges, n_qubits)
    sv = Statevector.from_instruction(qc)
    # We want to MAXIMIZE cuts, so MINIMIZE -⟨C⟩
    # ⟨C⟩ = Σ ⟨(1-ZiZj)/2⟩ = (|edges|/2) - ⟨Σ ZiZj/2⟩
    zz_exp = sv.expectation_value(C_op).real
    expected_cut = len(edges)/2 - zz_exp
    return -expected_cut  # minimize negative = maximize cut

# --- Compare p=1 and p=2 ---
for p in [1, 2, 3]:
    x0 = np.random.RandomState(42).randn(2 * p) * 0.5
    result = minimize(qaoa_cost, x0=x0, method='COBYLA',
                      options={'maxiter': 500})
    print(f"QAOA p={p}: expected cut = {-result.fun:.4f}  "
          f"(optimal = {best_cut}, ratio = {-result.fun/best_cut:.4f})")

# Show the p=2 solution in detail
p = 2
x0 = np.random.RandomState(42).randn(4) * 0.5
result = minimize(qaoa_cost, x0=x0, method='COBYLA', options={'maxiter': 500})
gammas_opt = result.x[:p]
betas_opt = result.x[p:]

qc_opt = qaoa_circuit(gammas_opt, betas_opt, edges, n_qubits)
sv_opt = Statevector.from_instruction(qc_opt)
probs = sv_opt.probabilities_dict()

print(f"\nTop states from p=2 QAOA circuit:")
for state, prob in sorted(probs.items(), key=lambda x: -x[1])[:6]:
    partition = state
    cut = sum(1 for i, j in edges if partition[i] != partition[j])
    print(f"  |{state}⟩: prob={prob:.4f}, cut={cut}")
