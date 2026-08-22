"""Solve a linear dispatch model with DC transmission-flow limits."""

import numpy as np
from scipy.optimize import linprog

base_mva = 100.0
bus_count = 3
slack_bus = 0
lines = [
    (0, 1, 0.20, 70.0),
    (0, 2, 0.25, 55.0),
    (1, 2, 0.30, 45.0),
]
generator_buses = np.array([0, 2])
generator_cost = np.array([16.0, 31.0])
generator_max = np.array([120.0, 90.0])
loads = np.array([0.0, 100.0, 20.0])


def build_ptdf():
    b_bus = np.zeros((bus_count, bus_count))
    b_line = np.zeros((len(lines), bus_count))
    for row, (left, right, reactance, _) in enumerate(lines):
        value = 1.0 / reactance
        b_bus[left, left] += value
        b_bus[right, right] += value
        b_bus[left, right] -= value
        b_bus[right, left] -= value
        b_line[row, left] = value
        b_line[row, right] = -value
    non_slack = [bus for bus in range(bus_count) if bus != slack_bus]
    ptdf = np.zeros((len(lines), bus_count))
    ptdf[:, non_slack] = (
        b_line[:, non_slack]
        @ np.linalg.inv(b_bus[np.ix_(non_slack, non_slack)])
    )
    return ptdf


ptdf = build_ptdf()
generator_flow = ptdf[:, generator_buses]
load_flow = ptdf @ (-loads / base_mva)
limits = np.array([line[3] for line in lines]) / base_mva

result = linprog(
    generator_cost,
    A_ub=np.vstack([generator_flow / base_mva, -generator_flow / base_mva]),
    b_ub=np.concatenate([limits - load_flow, limits + load_flow]),
    A_eq=np.ones((1, len(generator_buses))),
    b_eq=np.array([loads.sum()]),
    bounds=[(0.0, float(limit)) for limit in generator_max],
    method="highs",
)
if not result.success:
    raise RuntimeError(result.message)

injections = -loads.copy()
for bus, power in zip(generator_buses, result.x):
    injections[bus] += power
flows_mw = base_mva * (ptdf @ (injections / base_mva))

assert np.isclose(injections.sum(), 0.0)
assert np.all(np.abs(flows_mw) <= np.array([line[3] for line in lines]) + 1e-8)

print("dispatch_MW:", np.round(result.x, 6).tolist())
print(f"energy cost: ${result.fun:,.2f}")
for (left, right, _, limit), flow in zip(lines, flows_mw):
    print(f"line {left}-{right}: {flow:7.2f} MW within +/-{limit:.1f} MW")
print("balance_MW:", float(injections.sum()))
