"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.1 QUBO: The Language of Quantum Optimization
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_02_qubo_the_language_of_quantum_optimizatio.py
"""

import numpy as np

def build_qubo(linear_costs, quadratic_costs, constraint_lhs, constraint_rhs, penalty):
    """Build a QUBO matrix from an optimization problem.

    Args:
        linear_costs: dict {i: cost} for each variable
        quadratic_costs: dict {(i,j): cost} for variable pairs
        constraint_lhs: dict {i: coefficient} for equality constraint
        constraint_rhs: float, the target value
        penalty: float, weight for constraint violation

    Returns:
        Q: numpy array (QUBO matrix)
        offset: constant term (penalty * rhs²)
    """
    variables = sorted(set(linear_costs.keys()) |
                       {v for pair in quadratic_costs for v in pair} |
                       set(constraint_lhs.keys()))
    n = len(variables)
    idx = {v: i for i, v in enumerate(variables)}
    Q = np.zeros((n, n))

    # Objective: linear terms on diagonal
    for var, cost in linear_costs.items():
        Q[idx[var], idx[var]] += cost

    # Objective: quadratic terms on off-diagonal
    for (v1, v2), cost in quadratic_costs.items():
        i, j = idx[v1], idx[v2]
        if i > j:
            i, j = j, i
        Q[i, j] += cost

    # Constraint: (Σ a_i x_i - b)² = Σ a_i² x_i² - 2b Σ a_i x_i + b²
    #                                  + 2 Σ_{i<j} a_i a_j x_i x_j
    # (using x_i² = x_i for binary variables)
    for var, coeff in constraint_lhs.items():
        Q[idx[var], idx[var]] += penalty * (coeff**2 - 2 * constraint_rhs * coeff)

    for v1 in constraint_lhs:
        for v2 in constraint_lhs:
            i, j = idx[v1], idx[v2]
            if i < j:
                Q[i, j] += penalty * 2 * constraint_lhs[v1] * constraint_lhs[v2]

    offset = penalty * constraint_rhs**2
    return Q, offset, variables

# Example: 4-item knapsack
# Items: (weight, value) -- maximize value, constraint: total weight ≤ 10
items = {0: (3, 4), 1: (4, 5), 2: (5, 7), 3: (6, 8)}

# For QUBO, convert to: minimize -value subject to weight ≤ capacity
# Use slack variable s to convert inequality to equality:
# Σ w_i x_i + s = capacity (s encoded in binary)

# Simple approach: just penalize overweight, maximize value
linear = {i: -items[i][1] for i in items}  # negative value (minimizing)
quadratic = {}
constraint = {i: items[i][0] for i in items}  # weight coefficients

Q, offset, variables = build_qubo(linear, quadratic, constraint, 10, penalty=5)
print("Knapsack QUBO matrix:")
print(np.round(Q, 1))
print(f"Variables: {variables}")

# Brute-force solve
from itertools import product as iproduct
best_val = float('inf')
best_x = None
for bits in iproduct([0, 1], repeat=len(variables)):
    x = np.array(bits)
    val = x @ Q @ x + offset
    weight = sum(items[i][0] * bits[i] for i in items)
    value = sum(items[i][1] * bits[i] for i in items)
    if val < best_val:
        best_val = val
        best_x = bits
        best_weight = weight
        best_value = value

print(f"\nOptimal selection: {best_x}")
print(f"Weight: {best_weight}/10, Value: {best_value}, QUBO: {best_val:.0f}")
# Output:
# Knapsack QUBO matrix:
# [[-259.  120.  150.  180.]
#  [   0. -325.  200.  240.]
#  [   0.    0. -382.  300.]
#  [   0.    0.    0. -428.]]
# Variables: [0, 1, 2, 3]
#
# Optimal selection: (0, 1, 0, 1)
# Weight: 10/10, Value: 13, QUBO: -13
