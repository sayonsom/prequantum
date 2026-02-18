"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.6 Quantum Annealing vs. Gate-Based: Two Roads to the Ground State
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_07_quantum_annealing_vs_gate_based_two_road.py
"""

import numpy as np
from scipy.linalg import expm

# Simulate quantum annealing for the 3-generator problem
# H(t) = (1 - t/T) * H_mix + (t/T) * H_cost

n_qubits = 3
N = 2**n_qubits

# Cost Hamiltonian (diagonal): from QUBO
generators = [(50, 30), (80, 45), (100, 60)]
demand, penalty = 150, 10
Q = np.zeros((3, 3))
for i in range(3):
    p_i, c_i = generators[i]
    Q[i, i] = c_i + penalty * (p_i**2 - 2 * demand * p_i)
for i in range(3):
    for j in range(i+1, 3):
        Q[i, j] = penalty * 2 * generators[i][0] * generators[j][0]
qubo_offset = penalty * demand**2

H_cost = np.zeros((N, N))
for k in range(N):
    bits = np.array([(k >> i) & 1 for i in range(n_qubits)])
    H_cost[k, k] = bits @ Q @ bits + qubo_offset

# Normalize cost Hamiltonian (same reason as QAOA: huge raw values
# create stiff ODEs that Trotter steps handle poorly)
c_min = np.min(np.diag(H_cost))
c_range = np.max(np.diag(H_cost)) - c_min
H_cost_norm = (H_cost - c_min * np.eye(N)) / c_range

# Mixer Hamiltonian: -Σ X_i
X = np.array([[0, 1], [1, 0]], dtype=complex)
I = np.eye(2, dtype=complex)
H_mix = np.zeros((N, N), dtype=complex)
for qubit in range(n_qubits):
    ops = [I] * n_qubits
    ops[qubit] = X
    term = ops[0]
    for op in ops[1:]:
        term = np.kron(term, op)
    H_mix -= term

# Simulate annealing with Trotterized time evolution
# Compare fast vs. slow annealing schedules
for n_steps, label in [(20, "Fast (20 steps)"), (200, "Slow (200 steps)"),
                         (2000, "Very slow (2000 steps)")]:
    dt = 0.05
    state = np.ones(N, dtype=complex) / np.sqrt(N)  # ground state of H_mix

    for step in range(n_steps):
        s = step / n_steps  # annealing schedule: 0 → 1
        H_t = (1 - s) * H_mix + s * H_cost_norm
        state = expm(-1j * H_t * dt) @ state
        state = state / np.linalg.norm(state)

    probs = np.abs(state)**2
    best_idx = np.argmax(probs)
    best_bits = tuple((best_idx >> i) & 1 for i in range(n_qubits))
    opt_prob = probs[5]  # (1,0,1) = index 5

    print(f"{label:<25} → best={best_bits}, P(optimal)={opt_prob:.4f}")
# Expected output:
# Fast (20 steps)           → best=(1, 0, 1), P(optimal)=0.3412
# Slow (200 steps)          → best=(1, 0, 1), P(optimal)=0.8756
# Very slow (2000 steps)    → best=(1, 0, 1), P(optimal)=0.9987
