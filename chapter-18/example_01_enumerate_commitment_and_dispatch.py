"""Enumerate binary commitments and solve continuous economic dispatch."""

from itertools import product

import numpy as np
from scipy.optimize import linprog

names = np.array(["A", "B", "C"])
p_min = np.array([30.0, 20.0, 0.0])
p_max = np.array([120.0, 80.0, 60.0])
marginal_cost = np.array([18.0, 24.0, 41.0])
no_load_cost = np.array([90.0, 55.0, 20.0])
startup_cost = np.array([300.0, 180.0, 80.0])
initial_status = np.zeros(3, dtype=int)
demand = 150.0


def dispatch(status: np.ndarray):
    """Return the minimum-cost dispatch for one fixed commitment."""
    bounds = [
        (float(p_min[i] * status[i]), float(p_max[i] * status[i]))
        for i in range(len(status))
    ]
    return linprog(
        marginal_cost,
        A_eq=np.ones((1, len(status))),
        b_eq=np.array([demand]),
        bounds=bounds,
        method="highs",
    )


feasible = []
for bits in product((0, 1), repeat=len(names)):
    status = np.array(bits, dtype=int)
    result = dispatch(status)
    if not result.success:
        continue
    starts = np.maximum(status - initial_status, 0)
    fixed_cost = no_load_cost @ status + startup_cost @ starts
    total_cost = float(result.fun + fixed_cost)
    feasible.append((total_cost, status, result.x))

best_cost, best_status, best_power = min(feasible, key=lambda row: row[0])
assert np.isclose(best_power.sum(), demand)
assert np.all(best_power >= p_min * best_status - 1e-9)
assert np.all(best_power <= p_max * best_status + 1e-9)

print(f"Demand: {demand:.1f} MW")
print(f"Feasible commitments: {len(feasible)} of {2 ** len(names)}")
print("unit  on  dispatch_MW")
for name, on, power in zip(names, best_status, best_power):
    print(f"{name:>4}  {on:>2}  {power:11.1f}")
print(f"Verified production cost: ${best_cost:,.2f}")
