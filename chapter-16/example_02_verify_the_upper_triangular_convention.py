"""Example 16.2: validate one explicit upper-triangular QUBO convention."""

from itertools import product

import numpy as np


def validate_upper_triangular_qubo(
    linear: np.ndarray,
    quadratic: np.ndarray,
    constant: float,
) -> None:
    linear = np.asarray(linear, dtype=float)
    quadratic = np.asarray(quadratic, dtype=float)

    if linear.ndim != 1:
        raise ValueError("linear must be a one-dimensional coefficient vector")
    if quadratic.shape != (linear.size, linear.size):
        raise ValueError("quadratic must be square and match linear length")
    if not np.all(np.isfinite(linear)) or not np.all(np.isfinite(quadratic)):
        raise ValueError("all coefficients must be finite")
    if not np.isfinite(constant):
        raise ValueError("constant must be finite")
    if not np.allclose(np.diag(quadratic), 0.0, atol=1e-12):
        raise ValueError("diagonal coefficients belong in linear")
    if not np.allclose(np.tril(quadratic, -1), 0.0, atol=1e-12):
        raise ValueError("store every pair coefficient once, above the diagonal")


def energy(bits, linear, quadratic, constant) -> float:
    x = np.asarray(bits, dtype=float)
    if x.shape != linear.shape or not np.all(np.isin(x, (0.0, 1.0))):
        raise ValueError("bits must be a binary vector matching linear")
    return float(constant + linear @ x + x @ quadratic @ x)


linear = np.array([-47.0, -76.0, -82.0])
quadratic = np.array(
    [
        [0.0, 40.0, 60.0],
        [0.0, 0.0, 120.0],
        [0.0, 0.0, 0.0],
    ]
)
constant = 90.0

validate_upper_triangular_qubo(linear, quadratic, constant)
energies = {
    "".join(str(bit) for bit in bits): energy(bits, linear, quadratic, constant)
    for bits in product((0, 1), repeat=3)
}

print(f"validated_assignments={len(energies)}")
print(f"minimum={min(energies, key=energies.get)}")
print(f"minimum_energy={min(energies.values()):.1f}")

try:
    validate_upper_triangular_qubo(linear, quadratic + quadratic.T, constant)
except ValueError as exc:
    print(f"symmetric_input_rejected={exc}")

