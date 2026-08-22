"""Example 16.4: convert an upper-triangular QUBO to Ising coefficients."""

from itertools import product

import numpy as np


def qubo_to_ising(linear, quadratic, constant):
    """Use x_i = (1 - z_i) / 2 with z_i in {-1, +1}."""
    linear = np.asarray(linear, dtype=float)
    quadratic = np.asarray(quadratic, dtype=float)
    n = linear.size

    ising_constant = float(constant)
    h = np.zeros(n, dtype=float)
    J = np.zeros((n, n), dtype=float)

    for i, coefficient in enumerate(linear):
        ising_constant += coefficient / 2.0
        h[i] -= coefficient / 2.0

    for i in range(n):
        for j in range(i + 1, n):
            coefficient = quadratic[i, j]
            ising_constant += coefficient / 4.0
            h[i] -= coefficient / 4.0
            h[j] -= coefficient / 4.0
            J[i, j] += coefficient / 4.0

    return ising_constant, h, J


linear = np.array([-47.0, -76.0, -82.0])
quadratic = np.array(
    [
        [0.0, 40.0, 60.0],
        [0.0, 0.0, 120.0],
        [0.0, 0.0, 0.0],
    ]
)
constant = 90.0

ising_constant, h, J = qubo_to_ising(linear, quadratic, constant)
maximum_error = 0.0
minimum = None

for bits in product((0, 1), repeat=3):
    x = np.asarray(bits, dtype=float)
    z = 1.0 - 2.0 * x
    qubo_energy = constant + linear @ x + x @ quadratic @ x
    ising_energy = ising_constant + h @ z + z @ J @ z
    maximum_error = max(maximum_error, abs(float(qubo_energy - ising_energy)))
    candidate = (float(ising_energy), bits)
    if minimum is None or candidate < minimum:
        minimum = candidate

print(f"ising_constant={ising_constant:.1f}")
print(f"h={h.tolist()}")
print(f"J_upper={np.triu(J, 1).tolist()}")
print(f"maximum_assignment_error={maximum_error:.1e}")
print(f"ground_assignment={''.join(str(bit) for bit in minimum[1])}")
print(f"ground_energy={minimum[0]:.1f}")

