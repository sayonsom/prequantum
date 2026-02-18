"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.1 Multi-Period Unit Commitment
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_02_multi_period_unit_commitment.py
"""

import numpy as np

# 3 generators, 4 time periods (simplified from 24)
gen_data = {
    'Coal':    {'cap': 200, 'cost': 30, 'startup': 5000},
    'Gas':     {'cap': 150, 'cost': 50, 'startup': 1000},
    'Nuclear': {'cap': 300, 'cost': 20, 'startup': 20000},
}

demand = [250, 400, 350, 200]  # MW per period
T = len(demand)
names = list(gen_data.keys())
N = len(names)
n_vars = N * T  # total binary variables

caps = np.array([gen_data[g]['cap'] for g in names])
costs = np.array([gen_data[g]['cost'] for g in names])
startups = np.array([gen_data[g]['startup'] for g in names])

# Variable index: u_{g,t} → index g*T + t
def idx(g, t):
    return g * T + t

# Build QUBO
Q = np.zeros((n_vars, n_vars))
offset = 0.0
penalty = 500  # per-MW^2 demand violation

# 1. Operating cost: cost_g * cap_g * u_{g,t}
for g in range(N):
    for t in range(T):
        Q[idx(g,t), idx(g,t)] += costs[g] * caps[g]

# 2. Startup cost: startup_g * u_{g,t} * (1 - u_{g,t-1})
#    = startup_g * (u_{g,t} - u_{g,t} * u_{g,t-1})
#    Linear part goes on diagonal, cross-term is negative
for g in range(N):
    for t in range(1, T):
        Q[idx(g,t), idx(g,t)] += startups[g]          # u_{g,t} term
        i, j = sorted([idx(g,t), idx(g,t-1)])
        Q[i, j] -= startups[g]                          # -u_{g,t}*u_{g,t-1}
    # Period 0: assume all off initially, so startup if on
    Q[idx(g,0), idx(g,0)] += startups[g]

# 3. Demand constraint per period: (sum_g cap_g * u_{g,t} - demand_t)^2
for t in range(T):
    d = demand[t]
    offset += penalty * d**2
    for g in range(N):
        Q[idx(g,t), idx(g,t)] += penalty * (caps[g]**2 - 2 * d * caps[g])
        for g2 in range(g+1, N):
            i, j = sorted([idx(g,t), idx(g2,t)])
            Q[i, j] += penalty * 2 * caps[g] * caps[g2]

# Brute force is 2^12 = 4096 -- still tractable
best_val = np.inf
best_x = None
for bits in range(2**n_vars):
    x = np.array([(bits >> i) & 1 for i in range(n_vars)])
    val = x @ Q @ x + offset
    if val < best_val:
        best_val = val
        best_x = x

# Display schedule
print("Optimal Unit Commitment Schedule:")
print(f"{'Generator':<10}", end="")
for t in range(T):
    print(f"  t={t} ({demand[t]}MW)", end="")
print(f"  {'Startup$':>10}")
print("-" * 72)

total_cost = 0.0
for g in range(N):
    print(f"{names[g]:<10}", end="")
    gen_startups = 0
    for t in range(T):
        on = best_x[idx(g,t)]
        print(f"  {'  ON  ':>12}" if on else f"  {' off  ':>12}", end="")
        if on:
            total_cost += costs[g] * caps[g]
            # Startup: on at t, off at t-1 (or t=0)
            if t == 0 or not best_x[idx(g, t-1)]:
                gen_startups += startups[g]
    total_cost += gen_startups
    print(f"  {gen_startups:>10,}")

print(f"\nTotal cost: ${total_cost:,.0f}")
print(f"QUBO objective: {best_val:,.0f}")
# Output:
# Optimal Unit Commitment Schedule:
# Generator   t=0 (250MW)  t=1 (400MW)  t=2 (350MW)  t=3 (200MW)  Startup$
# ------------------------------------------------------------------------
# Coal            ON            ON            ON            ON         5,000
# Gas            off            ON            ON           off         1,000
# Nuclear        off           off           off           off             0
#
# Total cost: $45,000
# QUBO objective: 2,545,000
