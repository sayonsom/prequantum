"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_01_the_quick_win.py
"""

import numpy as np

# Three generators: [capacity_MW, cost_per_MWh, min_output_MW]
generators = {
    'Coal':    {'cap': 200, 'cost': 30, 'min': 100},
    'Gas':     {'cap': 150, 'cost': 50, 'min':  50},
    'Nuclear': {'cap': 300, 'cost': 20, 'min': 200},
}

demand = 350  # MW
penalty = 1000  # penalty weight for demand constraint

names = list(generators.keys())
n = len(names)
caps = np.array([generators[g]['cap'] for g in names])
costs = np.array([generators[g]['cost'] for g in names])

# QUBO: minimize cost of running generators
# subject to: total capacity of ON generators >= demand
# Variable u_g = 1 if generator g is on

# Cost term: sum(cost_g * cap_g * u_g) -- total generation cost
# Demand penalty: penalty * (sum(cap_g * u_g) - demand)^2
# But we want >= not ==, so penalize only shortfall

# Build QUBO matrix (from Ch. 16 pattern)
Q = np.zeros((n, n))

# Linear costs on diagonal: cost * capacity for each generator
for i in range(n):
    Q[i, i] += costs[i] * caps[i]

# Demand constraint as equality penalty: (sum cap_i * u_i - demand)^2
# Expand: sum_i sum_j cap_i*cap_j*u_i*u_j - 2*demand*sum_i cap_i*u_i + demand^2
for i in range(n):
    Q[i, i] += penalty * (caps[i]**2 - 2 * demand * caps[i])
    for j in range(i+1, n):
        Q[i, j] += penalty * 2 * caps[i] * caps[j]

offset = penalty * demand**2

# Brute force: try all 2^n combinations
print(f"{'Combination':<25} {'Cap (MW)':>10} {'Cost ($)':>10} {'QUBO':>12}")
print("-" * 60)

best_cost = np.inf
best_combo = None
for bits in range(2**n):
    x = np.array([(bits >> i) & 1 for i in range(n)])
    total_cap = np.sum(caps * x)
    gen_cost = np.sum(costs * caps * x)
    qubo_val = x @ Q @ x + offset

    label = '+'.join(names[i] for i in range(n) if x[i]) or '(none)'
    print(f"{label:<25} {total_cap:>10.0f} {gen_cost:>10.0f} {qubo_val:>12.0f}")

    if qubo_val < best_cost:
        best_cost = qubo_val
        best_combo = x

on_gens = [names[i] for i in range(n) if best_combo[i]]
print(f"\nOptimal: {'+'.join(on_gens)}")
print(f"Total capacity: {np.sum(caps * best_combo)} MW for {demand} MW demand")
print(f"Generation cost: ${np.sum(costs * caps * best_combo):,.0f}/hr")
# Output:
# Combination               Cap (MW)    Cost ($)        QUBO
# ------------------------------------------------------------
# (none)                          0          0   122500000
# Coal                          200       6000    22506000
# Gas                           150       7500    40007500
# Coal+Gas                      350      13500       13500
# Nuclear                       300       6000     2506000
# Coal+Nuclear                  500      12000    22512000
# Gas+Nuclear                   450      13500    10013500
# Coal+Gas+Nuclear              650      19500    90019500
#
# Optimal: Coal+Gas
# Total capacity: 350 MW for 350 MW demand
# Generation cost: $13,500/hr
