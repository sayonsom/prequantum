"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_09_break_this.py
"""

import numpy as np

# 2 generators, 3 time periods
caps = [100, 80]     # MW
costs = [25, 40]     # $/MWh
demand = [120, 150, 90]
N, T = 2, 3
penalty = 500

Q = np.zeros((N * T, N * T))
offset = 0.0

for g in range(N):
    for t in range(T):
        i = g * T + t
        Q[i, i] += costs[g] * caps[g]

# Demand constraint
for t in range(T):
    d = demand[t]
    offset += penalty * d**2
    for g in range(N):
        i = g * T + t
        Q[i, i] += penalty * (caps[g]**2 - 2 * d * caps[g])
        for g2 in range(g+1, N):
            # BUG: wrong index calculation
            j = g2 * T + t
            Q[g, g2] += penalty * 2 * caps[g] * caps[g2]  # uses g,g2 not i,j!

# Solve by brute force
best_val, best_x = np.inf, None
for bits in range(2**(N*T)):
    x = np.array([(bits >> k) & 1 for k in range(N*T)])
    val = x @ Q @ x + offset
    if val < best_val:
        best_val, best_x = val, x

for t in range(T):
    on = [f"Gen{g}" for g in range(N) if best_x[g*T+t]]
    print(f"t={t}: {'+'.join(on) or 'none'}, demand={demand[t]}")
