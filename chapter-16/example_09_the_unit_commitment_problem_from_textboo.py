"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.8 The Unit Commitment Problem: From Textbook to Grid Scale
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_09_the_unit_commitment_problem_from_textboo.py
"""

import numpy as np
from itertools import product

def unit_commitment_qubo(generators, demand_profile, penalty_demand=10,
                          penalty_ramp=5, penalty_minup=5):
    """Build a multi-period unit commitment QUBO.

    This is the problem IonQ/ORNL tackled in 2025.

    Variables: x_{g,t} ∈ {0,1} -- generator g ON at time t
    Objective: minimize Σ_{g,t} cost_g * x_{g,t}
    Constraints:
      1. Demand: Σ_g power_g * x_{g,t} = demand_t  (each period)
      2. Ramp: |x_{g,t} - x_{g,t-1}| limited (penalize frequent switching)
      3. Min-up: if turned on, stay on for min_up periods
    """
    n_gen = len(generators)
    n_periods = len(demand_profile)
    n_vars = n_gen * n_periods

    Q = np.zeros((n_vars, n_vars))
    total_offset = 0

    def var_idx(g, t):
        return g * n_periods + t

    # Objective: operating costs
    for g in range(n_gen):
        for t in range(n_periods):
            idx = var_idx(g, t)
            Q[idx, idx] += generators[g]['cost']

    # Constraint 1: demand balance each period
    for t in range(n_periods):
        d = demand_profile[t]
        for g in range(n_gen):
            idx = var_idx(g, t)
            p_g = generators[g]['power']
            Q[idx, idx] += penalty_demand * (p_g**2 - 2 * d * p_g)

        for g1 in range(n_gen):
            for g2 in range(g1+1, n_gen):
                i = var_idx(g1, t)
                j = var_idx(g2, t)
                Q[i, j] += penalty_demand * 2 * generators[g1]['power'] * generators[g2]['power']

        total_offset += penalty_demand * d**2

    # Constraint 2: ramp penalty (penalize state changes between periods)
    # x_{g,t}(1 - x_{g,t+1}) + x_{g,t+1}(1 - x_{g,t}) penalizes switching
    for g in range(n_gen):
        for t in range(n_periods - 1):
            i = var_idx(g, t)
            j = var_idx(g, t+1)
            # Penalize x_{g,t} XOR x_{g,t+1}
            # = x_{g,t} + x_{g,t+1} - 2*x_{g,t}*x_{g,t+1}
            Q[i, i] += penalty_ramp
            Q[j, j] += penalty_ramp
            if i < j:
                Q[i, j] -= 2 * penalty_ramp
            else:
                Q[j, i] -= 2 * penalty_ramp

    return Q, total_offset, n_vars

# Small UC instance: 3 generators, 4 time periods
gens = [
    {'name': 'Coal',  'power': 100, 'cost': 40, 'min_up': 2},
    {'name': 'Gas',   'power': 80,  'cost': 60, 'min_up': 1},
    {'name': 'Solar', 'power': 50,  'cost': 10, 'min_up': 1},
]
# Demand varies: morning ramp, peak, evening, night
demand = [120, 180, 150, 100]

Q, offset, n_vars = unit_commitment_qubo(gens, demand)
print(f"UC problem: {len(gens)} generators × {len(demand)} periods = {n_vars} variables")
print(f"Search space: 2^{n_vars} = {2**n_vars:,} combinations")

# Brute-force (feasible for 12 variables)
best_val = float('inf')
best_schedule = None
for bits in product([0, 1], repeat=n_vars):
    x = np.array(bits)
    val = x @ Q @ x + offset
    if val < best_val:
        best_val = val
        best_schedule = bits

# Display schedule
print(f"\nOptimal schedule (QUBO value = {best_val:.0f}):")
print(f"{'Period':<10}", end="")
for g in gens:
    print(f"{g['name']:<10}", end="")
print(f"{'Total MW':>10} {'Demand':>10}")
print("-" * 55)
for t in range(len(demand)):
    print(f"  t={t:<6}", end="")
    total_power = 0
    for g_idx, g in enumerate(gens):
        idx = g_idx * len(demand) + t
        status = "ON" if best_schedule[idx] else "off"
        if best_schedule[idx]:
            total_power += g['power']
        print(f"{status:<10}", end="")
    print(f"{total_power:>8} MW {demand[t]:>8} MW")
