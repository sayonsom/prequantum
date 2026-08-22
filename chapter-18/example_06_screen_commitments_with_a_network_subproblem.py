"""Screen commitment candidates with a network-constrained LP subproblem."""

from itertools import product

import numpy as np
from scipy.optimize import linprog

generator_buses = np.array([0, 0, 2])
p_max = np.array([80.0, 55.0, 70.0])
cost = np.array([15.0, 24.0, 34.0])
no_load = np.array([70.0, 35.0, 20.0])
loads = np.array([0.0, 100.0, 20.0])
ptdf = np.array(
    [
        [0.0, -0.6170212765957447, -0.2553191489361702],
        [0.0, -0.3829787234042553, -0.7446808510638298],
        [0.0, 0.3829787234042553, -0.2553191489361702],
    ]
)
line_limits = np.array([70.0, 55.0, 45.0])
base_flow = ptdf @ (-loads)
generator_flow = ptdf[:, generator_buses]


def network_dispatch(status: np.ndarray):
    return linprog(
        cost,
        A_ub=np.vstack([generator_flow, -generator_flow]),
        b_ub=np.concatenate([line_limits - base_flow, line_limits + base_flow]),
        A_eq=np.ones((1, len(status))),
        b_eq=np.array([loads.sum()]),
        bounds=[(0.0, float(p_max[i] * status[i])) for i in range(len(status))],
        method="highs",
    )


accepted = []
print("status  capacity_check  network_check")
for bits in product((0, 1), repeat=len(p_max)):
    status = np.array(bits, dtype=int)
    capacity_ok = bool(p_max @ status >= loads.sum())
    result = network_dispatch(status) if capacity_ok else None
    network_ok = bool(result is not None and result.success)
    print(f"{''.join(map(str, bits))}      {str(capacity_ok):>5}          {str(network_ok):>5}")
    if network_ok:
        total = float(result.fun + no_load @ status)
        accepted.append((total, status, result.x))

best_cost, best_status, best_dispatch = min(accepted, key=lambda row: row[0])
print("selected status:", best_status.tolist())
print("selected dispatch_MW:", np.round(best_dispatch, 6).tolist())
print(f"verified cost: ${best_cost:,.2f}")
