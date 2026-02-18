"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.5 Portfolio Optimization: A Real-World QUBO
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_06_portfolio_optimization_a_real_world_qubo.py
"""

import numpy as np
from itertools import product

# 5 assets: expected monthly returns (%)
returns = np.array([2.1, 1.5, 3.0, 0.8, 2.5])
asset_names = ["Tech", "Bonds", "Energy", "RealEst", "Crypto"]

# Covariance matrix (risk)
cov = np.array([
    [4.0, 0.5, 1.2, 0.3, 2.0],
    [0.5, 1.0, 0.2, 0.1, 0.3],
    [1.2, 0.2, 3.5, 0.4, 1.5],
    [0.3, 0.1, 0.4, 0.8, 0.2],
    [2.0, 0.3, 1.5, 0.2, 5.0],
])

# QUBO: minimize -return + risk_aversion * risk
# f(x) = -Σ r_i x_i + λ Σ_{i,j} cov_{ij} x_i x_j
risk_aversion = 0.5

n = len(returns)
Q = np.zeros((n, n))

# Return terms (diagonal, negative because we minimize)
for i in range(n):
    Q[i, i] -= returns[i]

# Risk terms (covariance)
for i in range(n):
    for j in range(n):
        if i == j:
            Q[i, i] += risk_aversion * cov[i, j]
        elif i < j:
            Q[i, j] += risk_aversion * cov[i, j]  # upper triangle

# Budget constraint: select exactly 3 assets
budget = 3
budget_penalty = 5.0
for i in range(n):
    Q[i, i] += budget_penalty * (1 - 2 * budget)
for i in range(n):
    for j in range(i+1, n):
        Q[i, j] += budget_penalty * 2

budget_offset = budget_penalty * budget**2

# Brute-force solve
print(f"{'Portfolio':<30} {'Return':>8} {'Risk':>8} {'QUBO':>10} {'Feasible':>10}")
print("-" * 70)
best_val = float('inf')
best_x = None
for bits in product([0, 1], repeat=n):
    x = np.array(bits)
    if sum(bits) == 0:
        continue
    ret = returns @ x
    risk = x @ cov @ x
    qubo_val = x @ Q @ x + budget_offset
    feasible = "YES" if sum(bits) == budget else ""
    selected = [asset_names[i] for i in range(n) if bits[i]]
    label = "+".join(selected)
    if sum(bits) == budget:  # only show feasible
        print(f"  {label:<28} {ret:>7.1f}% {risk:>7.2f} {qubo_val:>10.2f} {feasible:>10}")
    if qubo_val < best_val:
        best_val = qubo_val
        best_x = bits

selected = [asset_names[i] for i in range(n) if best_x[i]]
print(f"\nOptimal portfolio: {'+'.join(selected)}")
print(f"Expected return: {returns @ np.array(best_x):.1f}%")
print(f"Portfolio risk: {np.array(best_x) @ cov @ np.array(best_x):.2f}")
# Output (feasible portfolios only):
# Portfolio                       Return     Risk       QUBO   Feasible
# ----------------------------------------------------------------------
#   Tech+Bonds+Energy               6.6%    12.30      -1.40        YES
#   Tech+Bonds+RealEst              4.4%     7.60      -1.05        YES
#   Tech+Bonds+Crypto               6.1%    15.60       0.30        YES
#   Tech+Energy+RealEst             5.9%    12.10      -0.80        YES
#   Tech+Energy+Crypto              7.6%    21.90       1.00        YES
#   Tech+RealEst+Crypto             5.4%    14.80       0.75        YES
#   Bonds+Energy+RealEst            5.3%     6.70      -2.30        YES
#   Bonds+Energy+Crypto             7.0%    13.50      -1.25        YES
#   Bonds+RealEst+Crypto            4.8%     8.00      -1.10        YES
#   Energy+RealEst+Crypto           6.3%    13.50      -0.60        YES
#
# Optimal portfolio: Bonds+Energy+RealEst
# Expected return: 5.3%
# Portfolio risk: 6.70
