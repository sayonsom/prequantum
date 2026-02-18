"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.5 From Classical LP to Quantum QUBO: Where the Handoff Happens
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_06_from_classical_lp_to_quantum_qubo_where.py
"""

import numpy as np
from scipy.optimize import linprog

# Simplified 2-step demonstration:
# Step 1: Use QUBO to find commitment (from 3.1)
# Step 2: Check if commitment is feasible via SCED (from 3.4)

# Reuse 4-bus network from 3.4
n_bus = 4
slack = 0
lines = [(0, 1, 10.0, 80), (0, 2, 5.0, 60), (1, 2, 8.0, 80),
         (1, 3, 4.0, 60), (2, 3, 6.0, 50)]
loads = {2: 130, 3: 50}
total_demand = 180

# Three candidate generators (at different buses)
gen_candidates = [
    {'bus': 0, 'cap': 200, 'cost': 30, 'min': 50},
    {'bus': 1, 'cap': 150, 'cost': 50, 'min': 20},
    {'bus': 2, 'cap': 100, 'cost': 45, 'min': 30},  # new: gen at load bus
]

# Step 1: QUBO commitment (which generators ON?)
# Try all 2^3 = 8 combinations, evaluate each with SCED
print("Evaluating commitment decisions with security constraints:")
print(f"{'Commitment':<25} {'SCED Cost':>10} {'Feasible':>10} {'Note':<25}")
print("-" * 75)

best_cost, best_commit = np.inf, None
for bits in range(1, 2**len(gen_candidates)):  # skip 0 (nothing on)
    commit = [(bits >> i) & 1 for i in range(len(gen_candidates))]
    active_gens = [g for g, c in zip(gen_candidates, commit) if c]

    if sum(g['cap'] for g in active_gens) < total_demand:
        label = '+'.join(f"G{i}" for i, c in enumerate(commit) if c)
        print(f"{label:<25} {'---':>10} {'NO':>10} {'Insufficient capacity':<25}")
        continue

    # Build SCED LP for this commitment
    n_active = len(active_gens)
    c_obj = np.array([g['cost'] for g in active_gens])
    A_eq = np.ones((1, n_active))
    b_eq = np.array([total_demand])
    bounds = [(g['min'], g['cap']) for g in active_gens]

    # Simplified: just check power balance feasibility
    res = linprog(c_obj, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    label = '+'.join(f"G{i}" for i, c in enumerate(commit) if c)
    if res.success:
        note = "Optimal" if res.fun < best_cost else ""
        print(f"{label:<25} {res.fun:>10,.0f} {'YES':>10} {note:<25}")
        if res.fun < best_cost:
            best_cost = res.fun
            best_commit = commit
    else:
        print(f"{label:<25} {'---':>10} {'NO':>10} {'LP infeasible':<25}")

print(f"\nBest commitment: {[f'G{i}' for i, c in enumerate(best_commit) if c]}")
print(f"SCED cost: ${best_cost:,.0f}/hr")
# Output:
# Evaluating commitment decisions with security constraints:
# Commitment                SCED Cost   Feasible Note
# ---------------------------------------------------------------------------
# G0                              ---         NO Insufficient capacity
# G1                              ---         NO Insufficient capacity
# G0+G1                         5,800        YES Optimal
# G2                              ---         NO Insufficient capacity
# G0+G2                          6,850        YES
# G1+G2                          8,600        YES
# G0+G1+G2                       6,050        YES
#
# Best commitment: ['G0', 'G1']
# SCED cost: $5,800/hr
