"""Example 16.3: calibrate an equality-constraint penalty by enumeration."""

from itertools import product

import numpy as np


power_units = np.array([1.0, 2.0, 3.0])
operating_cost = np.array([3.0, 4.0, 8.0])
demand_units = 3.0


def evaluate(bits, penalty):
    x = np.asarray(bits, dtype=float)
    power = float(power_units @ x)
    objective = float(operating_cost @ x)
    energy = objective + penalty * (power - demand_units) ** 2
    return energy, np.isclose(power, demand_units, atol=1e-12)


penalties = [0.0, 1.0, 2.9, 3.0, 3.1, 10.0, 100.0]
print("penalty  best  energy  feasible  best_infeasible")
for penalty in penalties:
    rows = []
    for bits in product((0, 1), repeat=3):
        energy, feasible = evaluate(bits, penalty)
        rows.append((energy, bits, feasible))
    rows.sort(key=lambda row: (row[0], row[1]))
    best_energy, best_bits, best_feasible = rows[0]
    best_infeasible = min(row[0] for row in rows if not row[2])
    bit_text = "".join(str(bit) for bit in best_bits)
    print(
        f"{penalty:>7.1f}  {bit_text:>4}  {best_energy:>6.1f}  "
        f"{str(bool(best_feasible)):>8}  {best_infeasible:>15.1f}"
    )

print("strict_threshold=3.0; choose penalty > 3.0")

