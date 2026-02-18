"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.2 QUBO Penalty Tuning: The Art of Encoding Constraints
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_03_qubo_penalty_tuning_the_art_of_encoding.py
"""

import numpy as np

# Same 3-generator setup from 3.1 (single period for clarity)
caps = np.array([200, 150, 300])
costs = np.array([30, 50, 20])
demand = 350
n = 3

def solve_with_penalty(penalty):
    """Solve UC QUBO for a given penalty weight, return solution."""
    Q = np.zeros((n, n))
    for i in range(n):
        Q[i, i] += costs[i] * caps[i]
    for i in range(n):
        Q[i, i] += penalty * (caps[i]**2 - 2 * demand * caps[i])
        for j in range(i+1, n):
            Q[i, j] += penalty * 2 * caps[i] * caps[j]
    offset = penalty * demand**2

    best_val, best_x = np.inf, None
    for bits in range(2**n):
        x = np.array([(bits >> i) & 1 for i in range(n)])
        val = x @ Q @ x + offset
        if val < best_val:
            best_val, best_x = val, x.copy()

    total_cap = caps @ best_x
    gen_cost = (costs * caps) @ best_x
    feasible = (total_cap >= demand)
    return best_x, total_cap, gen_cost, feasible

# Sweep penalty values
print(f"{'Penalty':>10} {'Solution':<20} {'Cap (MW)':>10} {'Cost':>10} {'Feasible':>10}")
print("-" * 65)
names = ['Coal', 'Gas', 'Nuclear']
for pen in [0.01, 0.1, 1, 10, 100, 1000]:
    x, cap, cost, feas = solve_with_penalty(pen)
    combo = '+'.join(names[i] for i in range(n) if x[i]) or 'none'
    print(f"{pen:>10.2f} {combo:<20} {cap:>10.0f} {cost:>10.0f} {'YES' if feas else 'NO':>10}")
# Output:
# Penalty    Solution             Cap (MW)       Cost   Feasible
# -----------------------------------------------------------------
#      0.01 Nuclear                     300       6000         NO
#      0.10 Nuclear                     300       6000         NO
#      1.00 Coal+Gas                    350      13500        YES
#     10.00 Coal+Gas                    350      13500        YES
#    100.00 Coal+Gas                    350      13500        YES
#   1000.00 Coal+Gas                    350      13500        YES
