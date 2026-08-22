"""Solve a four-bus lossless DC power-flow teaching model."""

import numpy as np

base_mva = 100.0
lines = [
    (0, 1, 0.20, 80.0),
    (0, 2, 0.25, 70.0),
    (1, 2, 0.30, 60.0),
    (1, 3, 0.25, 55.0),
    (2, 3, 0.20, 65.0),
]
injections_mw = np.array([70.0, -30.0, -25.0, -15.0])
slack_bus = 0

b_bus = np.zeros((4, 4))
for left, right, reactance, _ in lines:
    susceptance = 1.0 / reactance
    b_bus[left, left] += susceptance
    b_bus[right, right] += susceptance
    b_bus[left, right] -= susceptance
    b_bus[right, left] -= susceptance

non_slack = [bus for bus in range(4) if bus != slack_bus]
angles = np.zeros(4)
angles[non_slack] = np.linalg.solve(
    b_bus[np.ix_(non_slack, non_slack)],
    injections_mw[non_slack] / base_mva,
)

flows = []
for left, right, reactance, limit in lines:
    flow = base_mva * (angles[left] - angles[right]) / reactance
    flows.append(flow)
    print(
        f"line {left}-{right}: flow={flow:7.2f} MW "
        f"limit={limit:5.1f} loading={abs(flow) / limit:6.1%}"
    )

reconstructed = base_mva * b_bus @ angles
assert np.isclose(injections_mw.sum(), 0.0)
assert np.allclose(reconstructed, injections_mw, atol=1e-10)

print("angles_deg:", np.round(np.degrees(angles), 4).tolist())
print(f"maximum absolute angle difference: {np.degrees(np.ptp(angles)):.4f} degrees")
print("nodal balance residual MW:", np.round(reconstructed - injections_mw, 12).tolist())
