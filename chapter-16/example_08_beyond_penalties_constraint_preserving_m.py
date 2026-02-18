"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.7 Beyond Penalties: Constraint-Preserving Mixers
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_08_beyond_penalties_constraint_preserving_m.py
"""

import numpy as np

def xy_mixer_qaoa(Q, qubo_offset, budget, p=2, n_restarts=20):
    """QAOA with XY ring mixer for 'select exactly k' constraints.

    The XY mixer H_mix = Σ_{i<j} (X_i X_j + Y_i Y_j) / 2
    preserves Hamming weight -- it swaps |01⟩ ↔ |10⟩ between qubits
    but never creates or destroys 1s. Starting from any state with
    Hamming weight = budget, the mixer only explores other states
    with the same Hamming weight.

    This eliminates the need for a budget penalty term entirely.
    """
    n = Q.shape[0]
    N = 2**n

    # Cost diagonal WITHOUT budget penalty (only objective)
    cost_raw = np.zeros(N)
    for k in range(N):
        bits = np.array([(k >> i) & 1 for i in range(n)])
        if sum(bits) == budget:
            cost_raw[k] = bits @ Q @ bits + qubo_offset
        else:
            cost_raw[k] = 1e6  # mark infeasible (won't be reached)

    # Build XY mixer for all adjacent pairs (ring topology)
    # (X_i X_j + Y_i Y_j)/2 swaps |01⟩_ij ↔ |10⟩_ij
    def apply_xy_mixer(state, beta):
        for i in range(n):
            j = (i + 1) % n  # ring
            new_state = state.copy()
            cos_b = np.cos(beta)
            sin_b = np.sin(beta)
            for k in range(N):
                bit_i = (k >> i) & 1
                bit_j = (k >> j) & 1
                if bit_i != bit_j:  # |01⟩ or |10⟩ -- swap subspace
                    partner = k ^ (1 << i) ^ (1 << j)
                    new_state[k] = cos_b * state[k] - 1j * sin_b * state[partner]
            state = new_state
        return state

    # Feasible cost values only (for normalization)
    feasible_costs = [cost_raw[k] for k in range(N)
                      if bin(k).count('1') == budget]
    c_min = min(feasible_costs)
    c_range = max(feasible_costs) - c_min if max(feasible_costs) > c_min else 1.0
    cost_diag = np.where(cost_raw < 1e5,
                         (cost_raw - c_min) / c_range * np.pi,
                         0)  # zero out infeasible (never reached)

    # Initial state: equal superposition over all weight-k states
    initial = np.zeros(N, dtype=complex)
    for k in range(N):
        if bin(k).count('1') == budget:
            initial[k] = 1.0
    initial /= np.linalg.norm(initial)

    from scipy.optimize import minimize as sp_minimize

    def expectation(params):
        gammas, betas = params[:p], params[p:]
        state = initial.copy()
        for layer in range(p):
            state = np.exp(-1j * gammas[layer] * cost_diag) * state
            state = apply_xy_mixer(state, betas[layer])
        probs = np.abs(state)**2
        return np.dot(probs, cost_diag)

    np.random.seed(42)
    best = None
    for _ in range(n_restarts):
        init = np.random.uniform(-np.pi, np.pi, 2 * p)
        res = sp_minimize(expectation, init, method='COBYLA',
                         options={'maxiter': 3000})
        if best is None or res.fun < best.fun:
            best = res

    # Extract result
    gammas, betas = best.x[:p], best.x[p:]
    state = initial.copy()
    for layer in range(p):
        state = np.exp(-1j * gammas[layer] * cost_diag) * state
        state = apply_xy_mixer(state, betas[layer])
    probs = np.abs(state)**2

    best_idx = np.argmax(probs)
    best_bits = tuple((best_idx >> i) & 1 for i in range(n))
    return best_bits, cost_raw[best_idx], probs

# Portfolio problem: select exactly 3 of 5 assets
# Rebuild Q WITHOUT the budget penalty
returns = np.array([2.1, 1.5, 3.0, 0.8, 2.5])
asset_names = ["Tech", "Bonds", "Energy", "RealEst", "Crypto"]
cov = np.array([
    [4.0, 0.5, 1.2, 0.3, 2.0],
    [0.5, 1.0, 0.2, 0.1, 0.3],
    [1.2, 0.2, 3.5, 0.4, 1.5],
    [0.3, 0.1, 0.4, 0.8, 0.2],
    [2.0, 0.3, 1.5, 0.2, 5.0],
])
risk_aversion = 0.5
n = 5
Q_obj = np.zeros((n, n))
for i in range(n):
    Q_obj[i, i] -= returns[i]
for i in range(n):
    for j in range(n):
        if i == j:
            Q_obj[i, i] += risk_aversion * cov[i, j]
        elif i < j:
            Q_obj[i, j] += risk_aversion * cov[i, j]

best_bits, best_cost, probs = xy_mixer_qaoa(Q_obj, 0, budget=3, p=3)
selected = [asset_names[i] for i in range(n) if best_bits[i]]
print(f"XY-mixer QAOA optimal: {'+'.join(selected)}")
print(f"\nFeasible state probabilities:")
for k in range(2**n):
    bits = tuple((k >> i) & 1 for i in range(n))
    if sum(bits) == 3 and probs[k] > 0.01:
        sel = [asset_names[i] for i in range(n) if bits[i]]
        print(f"  {'+'.join(sel):<30} P={probs[k]:.4f}")
# The XY mixer searches ONLY among 3-asset portfolios,
# so every state it visits is feasible. No penalty tuning needed.
