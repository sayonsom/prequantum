"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.3 DC Power Flow: When Physics Constrains Optimization
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_04_dc_power_flow_when_physics_constrains_op.py
"""

import numpy as np

# Simple 4-bus network (per-unit system, base = 100 MVA)
#   Bus 0: Slack (reference, theta=0) -- cheap generator
#   Bus 1: Generator (20 MW minimum dispatch)
#   Bus 2: Load (130 MW)
#   Bus 3: Load (50 MW)
#
# Lines: 0-1 (b=10pu), 0-2 (b=5pu), 1-2 (b=8pu), 1-3 (b=4pu), 2-3 (b=6pu)

n_bus = 4
slack = 0  # reference bus
base_mva = 100  # per-unit base

# Line data: (from, to, susceptance_pu, limit_MW)
lines = [
    (0, 1, 10.0, 80),
    (0, 2,  5.0, 60),
    (1, 2,  8.0, 80),
    (1, 3,  4.0, 60),
    (2, 3,  6.0, 50),
]

# Build B matrix (susceptance matrix, per-unit)
B = np.zeros((n_bus, n_bus))
for (i, j, b, _) in lines:
    B[i, i] += b
    B[j, j] += b
    B[i, j] -= b
    B[j, i] -= b

print("Susceptance matrix B (per-unit):")
print(np.round(B, 1))

# Power injections in MW -- cheap gen at bus 0 maxed out (naive dispatch)
# Bus 0 is slack: its injection balances the system
P_mw = np.array([0, 20, -130, -50], dtype=float)
P_pu = P_mw / base_mva  # convert to per-unit for solving

# Remove slack bus row/col for solving
non_slack = [i for i in range(n_bus) if i != slack]
B_reduced = B[np.ix_(non_slack, non_slack)]
P_reduced = P_pu[non_slack]

# Solve: theta = B_inv * P (for non-slack buses)
theta_reduced = np.linalg.solve(B_reduced, P_reduced)
theta = np.zeros(n_bus)
theta[non_slack] = theta_reduced

# Slack bus power: P_slack = B[slack,:] @ theta (row of B times angle vector)
P_slack_pu = B[slack, :] @ theta
P_mw[slack] = P_slack_pu * base_mva

print(f"\nBus results:")
for i in range(n_bus):
    role = "Slack" if i == slack else ("Gen" if P_mw[i] > 0 else "Load")
    deg = np.degrees(theta[i])
    print(f"  Bus {i} ({role:>5}): theta = {theta[i]:+.4f} rad ({deg:+.2f} deg),"
          f" P = {P_mw[i]:+.1f} MW")

# Line flows
print(f"\nLine flows:")
print(f"{'Line':<10} {'Flow (MW)':>10} {'Limit (MW)':>10} {'Loading':>10}")
print("-" * 50)
for (i, j, b, limit) in lines:
    flow_pu = b * (theta[i] - theta[j])
    flow_mw = flow_pu * base_mva
    loading = abs(flow_mw) / limit * 100
    flag = " ** OVERLOADED" if loading > 100 else (" ** CONGESTED" if loading > 90 else "")
    print(f"  {i}-{j}      {flow_mw:>+10.1f} {limit:>10.0f} {loading:>9.1f}%{flag}")

print(f"\nPower balance: {sum(P_mw):.1f} MW (should be 0)")
# Output:
# Susceptance matrix B (per-unit):
# [[ 15. -10.  -5.   0.]
#  [-10.  22.  -8.  -4.]
#  [ -5.  -8.  19.  -6.]
#  [  0.  -4.  -6.  10.]]
#
# Bus results:
#   Bus 0 (Slack): theta = +0.0000 rad (+0.00 deg), P = +160.0 MW
#   Bus 1 (  Gen): theta = -0.0808 rad (-4.63 deg), P = +20.0 MW
#   Bus 2 ( Load): theta = -0.1584 rad (-9.08 deg), P = -130.0 MW
#   Bus 3 ( Load): theta = -0.1774 rad (-10.16 deg), P = -50.0 MW
#
# Line flows:
# Line        Flow (MW)  Limit (MW)    Loading
# --------------------------------------------------
#   0-1           +80.8         80     101.0% ** OVERLOADED
#   0-2           +79.2         60     132.0% ** OVERLOADED
#   1-2           +62.1         80      77.7%
#   1-3           +38.6         60      64.4%
#   2-3           +11.4         50      22.7%
#
# Power balance: 0.0 MW (should be 0)
