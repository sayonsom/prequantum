"""Enumerate commitments for a small multi-period scheduling reference."""

from itertools import product

import numpy as np
from scipy.optimize import linprog

names = ("A", "B")
demand = np.array([70.0, 125.0, 85.0])
p_min = np.array([30.0, 10.0])
p_max = np.array([100.0, 60.0])
ramp = np.array([45.0, 60.0])
energy_cost = np.array([19.0, 32.0])
no_load = np.array([50.0, 20.0])
startup = np.array([160.0, 70.0])
initial_status = np.array([1, 0], dtype=int)
initial_power = np.array([55.0, 0.0])
periods = len(demand)
units = len(names)


def dispatch_for(status: np.ndarray):
    """Solve continuous dispatch for a fixed [period, unit] status matrix."""
    variable_count = periods * units
    objective = np.tile(energy_cost, periods)
    a_eq = np.zeros((periods, variable_count))
    for t in range(periods):
        a_eq[t, t * units : (t + 1) * units] = 1.0

    a_ub = []
    b_ub = []
    for t in range(periods):
        for g in range(units):
            row_up = np.zeros(variable_count)
            row_down = np.zeros(variable_count)
            index = t * units + g
            row_up[index] = 1.0
            row_down[index] = -1.0
            if t == 0:
                a_ub.extend([row_up, row_down])
                b_ub.extend([ramp[g] + initial_power[g], ramp[g] - initial_power[g]])
            else:
                previous = (t - 1) * units + g
                row_up[previous] = -1.0
                row_down[previous] = 1.0
                a_ub.extend([row_up, row_down])
                b_ub.extend([ramp[g], ramp[g]])

    bounds = [
        (float(p_min[g] * status[t, g]), float(p_max[g] * status[t, g]))
        for t in range(periods)
        for g in range(units)
    ]
    return linprog(
        objective,
        A_ub=np.asarray(a_ub),
        b_ub=np.asarray(b_ub),
        A_eq=a_eq,
        b_eq=demand,
        bounds=bounds,
        method="highs",
    )


candidates = []
for flat_bits in product((0, 1), repeat=periods * units):
    status = np.array(flat_bits, dtype=int).reshape(periods, units)
    result = dispatch_for(status)
    if not result.success:
        continue
    previous = np.vstack([initial_status, status[:-1]])
    starts = np.maximum(status - previous, 0)
    fixed = float(np.sum(status * no_load) + np.sum(starts * startup))
    candidates.append((float(result.fun + fixed), status, result.x.reshape(periods, units)))

best_cost, best_status, best_dispatch = min(candidates, key=lambda row: row[0])
assert np.allclose(best_dispatch.sum(axis=1), demand)
assert np.all(np.abs(np.diff(np.vstack([initial_power, best_dispatch]), axis=0)) <= ramp + 1e-9)

print(f"Feasible schedules: {len(candidates)} of {2 ** (periods * units)}")
print("period demand  A_on A_MW  B_on B_MW")
for t in range(periods):
    print(
        f"{t:>6} {demand[t]:>6.1f}"
        f" {best_status[t, 0]:>5} {best_dispatch[t, 0]:>4.1f}"
        f" {best_status[t, 1]:>5} {best_dispatch[t, 1]:>4.1f}"
    )
print(f"Verified schedule cost: ${best_cost:,.2f}")
