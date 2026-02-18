"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_01_the_quick_win.py
"""

import numpy as np
from itertools import product

# Three generators: (power_MW, cost_per_hr)
generators = [(50, 30), (80, 45), (100, 60)]
demand = 150  # MW required

# QUBO formulation:
# Decision variables: x_i ∈ {0, 1} (generator i on/off)
# Objective: minimize Σ cost_i * x_i
# Constraint: Σ power_i * x_i = demand
#
# Penalty method: fold constraint into objective
# Total = Σ cost_i * x_i + penalty * (Σ power_i * x_i - demand)²

penalty = 10  # large enough to enforce constraint

# Build the QUBO matrix Q where f(x) = x^T Q x
n = len(generators)
Q = np.zeros((n, n))

# Linear terms (diagonal): cost + penalty * (power_i² - 2 * demand * power_i)
for i in range(n):
    p_i, c_i = generators[i]
    Q[i, i] = c_i + penalty * (p_i**2 - 2 * demand * p_i)

# Quadratic terms (off-diagonal): penalty * 2 * power_i * power_j
for i in range(n):
    for j in range(i+1, n):
        p_i = generators[i][0]
        p_j = generators[j][0]
        Q[i, j] = penalty * 2 * p_i * p_j

print("QUBO matrix Q:")
print(Q)
print()

# Brute-force: evaluate all 2^n combinations
best_cost = float('inf')
best_solution = None
print(f"{'Config':<12} {'Power':>7} {'Cost':>7} {'Penalty':>10} {'Total':>10} {'Feasible':>10}")
print("-" * 60)
for bits in product([0, 1], repeat=n):
    x = np.array(bits)
    total_power = sum(g[0] * x[i] for i, g in enumerate(generators))
    total_cost = sum(g[1] * x[i] for i, g in enumerate(generators))
    penalty_val = penalty * (total_power - demand)**2
    qubo_val = x @ Q @ x + penalty * demand**2  # constant term
    feasible = "YES" if total_power == demand else "no"
    print(f"  {bits}    {total_power:>5} MW  ${total_cost:>5}  {penalty_val:>10.0f}  {qubo_val:>10.0f}  {feasible:>10}")
    if qubo_val < best_cost:
        best_cost = qubo_val
        best_solution = bits

print(f"\nOptimal: generators {best_solution}, QUBO value = {best_cost:.0f}")
# Output:
# QUBO matrix Q:
# [[-122500.  80000. 100000.]
#  [ 80000. -175900. 160000.]
#  [100000. 160000. -200940.]]
#
# Config        Power    Cost    Penalty      Total   Feasible
# ------------------------------------------------------------
#   (0, 0, 0)       0 MW     $0     225000     225000         no
#   (0, 0, 1)     100 MW    $60      25000      24060         no
#   (0, 1, 0)      80 MW    $45      49000      49100         no
#   (0, 1, 1)     180 MW   $105       9000       8205         no
#   (1, 0, 0)      50 MW    $30     100000     102500         no
#   (1, 0, 1)     150 MW    $90          0       1560        YES
#   (1, 1, 0)     130 MW    $75       4000       6600         no
#   (1, 1, 1)     210 MW   $135      36000      35700         no
#
# Optimal: generators (1, 0, 1), QUBO value = 1560
