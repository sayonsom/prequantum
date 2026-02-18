"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.4 Security-Constrained Dispatch
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_05_security_constrained_dispatch.py
"""

import numpy as np
from scipy.optimize import linprog

# Same 4-bus network from 3.3
n_bus = 4
slack = 0

lines = [
    (0, 1, 10.0, 80),
    (0, 2,  5.0, 60),
    (1, 2,  8.0, 80),
    (1, 3,  4.0, 60),
    (2, 3,  6.0, 50),
]
n_lines = len(lines)

# Generators: bus, min_MW, max_MW, cost_per_MWh
gens = [
    (0, 50, 200, 30),   # Cheap coal at bus 0
    (1, 20, 150, 50),   # Expensive gas at bus 1
]
n_gens = len(gens)

# Loads (same as 3.3)
loads = {2: 130, 3: 50}  # bus: MW
total_demand = sum(loads.values())  # 180 MW

# Build B matrix (same as 3.3)
B = np.zeros((n_bus, n_bus))
for (i, j, b, _) in lines:
    B[i, i] += b
    B[j, j] += b
    B[i, j] -= b
    B[j, i] -= b

# Power Transfer Distribution Factors (PTDF)
# PTDF tells us: if 1 MW is injected at bus k and withdrawn at slack,
# how much flows on each line?
non_slack = [i for i in range(n_bus) if i != slack]
B_reduced = B[np.ix_(non_slack, non_slack)]
B_inv = np.linalg.inv(B_reduced)

# Build PTDF matrix: n_lines x n_bus
PTDF = np.zeros((n_lines, n_bus))
for l_idx, (i, j, b_line, _) in enumerate(lines):
    for k in range(n_bus):
        if k == slack:
            continue
        k_red = non_slack.index(k)  # index in reduced system
        theta_i = B_inv[non_slack.index(i), k_red] if i != slack else 0
        theta_j = B_inv[non_slack.index(j), k_red] if j != slack else 0
        PTDF[l_idx, k] = b_line * (theta_i - theta_j)

print("Power Transfer Distribution Factors (PTDF):")
print(f"{'Line':<8}", end="")
for k in range(n_bus):
    print(f"  Bus {k:>2}", end="")
print()
for l_idx, (i, j, _, _) in enumerate(lines):
    print(f"  {i}-{j}   ", end="")
    for k in range(n_bus):
        print(f"  {PTDF[l_idx, k]:>+6.3f}", end="")
    print()

# Formulate as LP: minimize cost subject to line limits
# Decision variables: P_g for each generator (MW output)
# Objective: min sum(cost_g * P_g)
c = np.array([g[3] for g in gens], dtype=float)

# Equality: sum(P_g) = total_demand
A_eq = np.ones((1, n_gens))
b_eq = np.array([total_demand])

# Bounds: min_g <= P_g <= max_g
bounds = [(g[1], g[2]) for g in gens]

# Line flow constraints using PTDF
# Flow on line l = sum_k PTDF[l,k] * P_net[k]
# P_net[k] = generation at k - load at k
# For each line: -limit <= flow <= limit
A_ub = []
b_ub = []

for l_idx, (_, _, _, limit) in enumerate(lines):
    # Constant flow from loads (negative injections)
    load_flow = sum(PTDF[l_idx, bus] * (-load_mw) for bus, load_mw in loads.items())

    # Generator contribution coefficients
    gen_coeffs = np.array([PTDF[l_idx, g[0]] for g in gens])

    # flow = gen_coeffs @ P_g + load_flow <= limit
    A_ub.append(gen_coeffs)
    b_ub.append(limit - load_flow)

    # -flow <= limit  →  -gen_coeffs @ P_g - load_flow <= limit
    A_ub.append(-gen_coeffs)
    b_ub.append(limit + load_flow)

A_ub = np.array(A_ub)
b_ub = np.array(b_ub)

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                 bounds=bounds, method='highs')

print(f"\nOptimal Dispatch (Security-Constrained):")
print(f"  Total demand: {total_demand} MW")
for g_idx, (bus, pmin, pmax, cost) in enumerate(gens):
    print(f"  Gen at bus {bus}: {result.x[g_idx]:.1f} MW "
          f"(range {pmin}-{pmax}), cost=${cost}/MWh")
print(f"  Total cost: ${result.fun:,.0f}/hr")

# Compare with unconstrained economic dispatch
result_unc = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
print(f"\n  Unconstrained cost: ${result_unc.fun:,.0f}/hr"
      f" (P0={result_unc.x[0]:.0f}, P1={result_unc.x[1]:.0f})")
print(f"  Congestion cost: ${result.fun - result_unc.fun:,.0f}/hr")

# Verify line flows
P_net = np.zeros(n_bus)
for g_idx, (bus, _, _, _) in enumerate(gens):
    P_net[bus] += result.x[g_idx]
for bus, load_mw in loads.items():
    P_net[bus] -= load_mw

print(f"\nLine flows with security constraints:")
print(f"{'Line':<8} {'Flow':>8} {'Limit':>8} {'Loading':>8}")
print("-" * 36)
for l_idx, (i, j, b_line, limit) in enumerate(lines):
    flow = sum(PTDF[l_idx, k] * P_net[k] for k in range(n_bus))
    loading = abs(flow) / limit * 100
    flag = " BINDING" if loading > 99 else ""
    print(f"  {i}-{j}    {flow:>+7.1f}  {limit:>7.0f}  {loading:>6.1f}%{flag}")
# Output:
# Power Transfer Distribution Factors (PTDF):
# Line      Bus  0  Bus  1  Bus  2  Bus  3
#   0-1     +0.000  -0.748  -0.505  -0.602
#   0-2     +0.000  -0.252  -0.495  -0.398
#   1-2     +0.000  +0.194  -0.388  -0.155
#   1-3     +0.000  +0.058  -0.117  -0.447
#   2-3     +0.000  -0.058  +0.117  -0.553
#
# Optimal Dispatch (Security-Constrained):
#   Total demand: 180 MW
#   Gen at bus 0: 83.8 MW (range 50-200), cost=$30/MWh
#   Gen at bus 1: 96.2 MW (range 20-150), cost=$50/MWh
#   Total cost: $7,323/hr
#
#   Unconstrained cost: $5,800/hr (P0=160, P1=20)
#   Congestion cost: $1,523/hr
#
# Line flows with security constraints:
# Line       Flow    Limit  Loading
# ------------------------------------
#   0-1      +23.8       80    29.8%
#   0-2      +60.0       60   100.0% BINDING
#   1-2      +76.9       80    96.2%
#   1-3      +43.1       60    71.8%
#   2-3       +6.9       50    13.8%
