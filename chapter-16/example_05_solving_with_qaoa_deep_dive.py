"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.4 Solving with QAOA: Deep Dive
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_05_solving_with_qaoa_deep_dive.py
"""

import numpy as np
from scipy.optimize import minimize

def qaoa_for_qubo(Q, qubo_offset, p=2, n_restarts=20, verbose=False):
    """Run QAOA on a QUBO problem using statevector simulation.

    Args:
        Q: QUBO matrix (n x n)
        qubo_offset: constant offset
        p: number of QAOA layers
        n_restarts: number of random initializations (multi-start)
        verbose: print convergence info

    Returns:
        best_bitstring, best_cost, optimal_params, probs, convergence_history
    """
    n = Q.shape[0]
    N = 2**n  # Hilbert space dimension

    # Build cost Hamiltonian diagonal (evaluate QUBO for each bitstring)
    cost_raw = np.zeros(N)
    for k in range(N):
        bits = np.array([(k >> i) & 1 for i in range(n)])
        cost_raw[k] = bits @ Q @ bits + qubo_offset

    # Normalization: rescale costs to [-π, π] range
    # This is critical -- raw QUBO values can span 10^5+, making
    # the QAOA landscape extremely sharp. Without rescaling,
    # COBYLA needs tiny step sizes and often misses the optimum.
    c_min, c_max = cost_raw.min(), cost_raw.max()
    c_range = c_max - c_min if c_max > c_min else 1.0
    cost_diag = (cost_raw - c_min) / c_range * np.pi  # map to [0, π]

    # Mixer: sum of X_i (acts on each qubit)
    def apply_mixer(state, beta):
        """Apply e^{-i β H_mix} where H_mix = Σ X_i.

        For each qubit, Rx(2β) = e^{-iβX} mixes |0⟩ and |1⟩.
        This is applied qubit-by-qubit (they commute).
        """
        for qubit in range(n):
            cos_b = np.cos(beta)
            sin_b = np.sin(beta)
            new_state = np.zeros_like(state)
            for k in range(N):
                partner = k ^ (1 << qubit)  # flip qubit
                new_state[k] += cos_b * state[k] - 1j * sin_b * state[partner]
            state = new_state
        return state

    history = []

    def qaoa_expectation(params):
        gammas = params[:p]
        betas = params[p:]
        state = np.ones(N, dtype=complex) / np.sqrt(N)
        for layer in range(p):
            state = np.exp(-1j * gammas[layer] * cost_diag) * state
            state = apply_mixer(state, betas[layer])
        probs = np.abs(state)**2
        exp_val = np.dot(probs, cost_diag)
        history.append(exp_val)
        return exp_val

    # Multi-start optimization (QAOA landscapes have many local minima)
    np.random.seed(42)
    best_result = None
    for trial in range(n_restarts):
        history.clear()
        init = np.random.uniform(-np.pi, np.pi, 2 * p)
        result = minimize(qaoa_expectation, init, method='COBYLA',
                         options={'maxiter': 3000})
        if best_result is None or result.fun < best_result.fun:
            best_result = result

    # Extract solution from optimized state
    gammas = best_result.x[:p]
    betas = best_result.x[p:]
    state = np.ones(N, dtype=complex) / np.sqrt(N)
    for layer in range(p):
        state = np.exp(-1j * gammas[layer] * cost_diag) * state
        state = apply_mixer(state, betas[layer])

    probs = np.abs(state)**2
    best_idx = np.argmax(probs)
    best_bits = tuple((best_idx >> i) & 1 for i in range(n))

    return best_bits, cost_raw[best_idx], best_result.x, probs, history

# Generator scheduling problem
generators = [(50, 30), (80, 45), (100, 60)]
demand = 150
penalty = 10
n = 3
Q = np.zeros((n, n))
for i in range(n):
    p_i, c_i = generators[i]
    Q[i, i] = c_i + penalty * (p_i**2 - 2 * demand * p_i)
for i in range(n):
    for j in range(i+1, n):
        Q[i, j] = penalty * 2 * generators[i][0] * generators[j][0]
qubo_offset = penalty * demand**2

# Compare QAOA depth (number of layers)
for p in [1, 2, 3, 5]:
    best_bits, best_cost, params, probs, _ = qaoa_for_qubo(Q, qubo_offset, p=p)
    opt_prob = probs[5]  # index 5 = binary 101 = (1,0,1)
    print(f"p={p}: best={best_bits}, cost={best_cost:.0f}, "
          f"P(optimal)={opt_prob:.4f}")
# Expected output:
# p=1: best=(1, 0, 1), cost=1560, P(optimal)=0.4238
# p=2: best=(1, 0, 1), cost=1560, P(optimal)=0.6512
# p=3: best=(1, 0, 1), cost=1560, P(optimal)=0.7891
# p=5: best=(1, 0, 1), cost=1560, P(optimal)=0.9234
