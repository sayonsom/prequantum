"""Verify a small capacity-selection QUBO over its complete state space."""

from itertools import product

import numpy as np

capacity = np.array([50, 40, 30], dtype=int)
normalized_cost = np.array([6, 5, 4], dtype=int)
demand = 70
surplus_weights = np.array([10, 20, 40], dtype=int)


def decode(bits):
    x = np.array(bits[:3], dtype=int)
    s_bits = np.array(bits[3:], dtype=int)
    supply = int(capacity @ x)
    surplus = int(surplus_weights @ s_bits)
    residual = supply - demand - surplus
    objective = int(normalized_cost @ x)
    return x, surplus, residual, objective


states = []
for bits in product((0, 1), repeat=6):
    x, surplus, residual, objective = decode(bits)
    states.append(
        {
            "bits": bits,
            "x": x,
            "surplus": surplus,
            "residual": residual,
            "objective": objective,
        }
    )

feasible_states = [state for state in states if state["residual"] == 0]
best_feasible = min(feasible_states, key=lambda state: state["objective"])
required = [
    (best_feasible["objective"] - state["objective"])
    / (state["residual"] ** 2)
    for state in states
    if state["residual"] != 0
    and state["objective"] < best_feasible["objective"]
]
strict_threshold = max(required, default=0.0)

print(
    "Best feasible selection:",
    best_feasible["x"].tolist(),
    "surplus_MW:",
    best_feasible["surplus"],
    "cost:",
    best_feasible["objective"],
)
print(f"Penalty must be strictly greater than {strict_threshold:.6f}")

for penalty in (0.001, strict_threshold, strict_threshold + 0.001, 1.0):
    energies = [
        state["objective"] + penalty * state["residual"] ** 2
        for state in states
    ]
    ground_energy = min(energies)
    ground_states = [
        state
        for state, energy in zip(states, energies)
        if np.isclose(energy, ground_energy)
    ]
    all_feasible = all(state["residual"] == 0 for state in ground_states)
    print(
        f"lambda={penalty:8.6f}",
        f"ground_states={len(ground_states)}",
        f"all_feasible={all_feasible}",
    )

assert np.isclose(strict_threshold, 0.0075)
assert all(state["residual"] == 0 for state in ground_states)
