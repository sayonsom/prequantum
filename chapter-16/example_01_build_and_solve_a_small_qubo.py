"""Example 16.1: compile and solve a small generator-selection QUBO."""

from itertools import product

import numpy as np


# One power unit represents 50 MW. The scale keeps the example readable.
power_units = np.array([1.0, 2.0, 3.0])
operating_cost = np.array([3.0, 4.0, 8.0])
demand_units = 3.0
penalty = 10.0

# Upper-triangular convention:
# E(x) = constant + linear @ x + x @ quadratic @ x.
# Diagonal coefficients are stored in `linear`; each pair coefficient appears
# once in the strict upper triangle of `quadratic`.
linear = operating_cost + penalty * (
    power_units**2 - 2.0 * demand_units * power_units
)
quadratic = np.zeros((3, 3), dtype=float)
for i in range(3):
    for j in range(i + 1, 3):
        quadratic[i, j] = 2.0 * penalty * power_units[i] * power_units[j]
constant = penalty * demand_units**2


def direct_energy(x: np.ndarray) -> float:
    mismatch = power_units @ x - demand_units
    return float(operating_cost @ x + penalty * mismatch**2)


def qubo_energy(x: np.ndarray) -> float:
    return float(constant + linear @ x + x @ quadratic @ x)


rows = []
for bits in product((0, 1), repeat=3):
    x = np.asarray(bits, dtype=float)
    direct = direct_energy(x)
    compiled = qubo_energy(x)
    assert np.isclose(direct, compiled, atol=1e-12)
    rows.append(
        (
            "".join(str(bit) for bit in bits),
            int(power_units @ x),
            int(operating_cost @ x),
            int((power_units @ x - demand_units) ** 2),
            int(compiled),
        )
    )

print("bits  power  cost  mismatch^2  QUBO")
for row in rows:
    print(f"{row[0]:>4}  {row[1]:>5}  {row[2]:>4}  {row[3]:>10}  {row[4]:>4}")

best = min(rows, key=lambda row: row[-1])
print(f"best={best[0]}, power_units={best[1]}, operating_cost={best[2]}")

