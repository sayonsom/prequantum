"""Compare a product-state quantum kernel with its exact classical formula."""

import numpy as np


def product_angle_state(features):
    """Map finite real features to product states with angles pi*x_j."""
    features = np.asarray(features, dtype=float)
    if features.ndim != 1 or not np.all(np.isfinite(features)):
        raise ValueError("features must be a finite one-dimensional array")
    state = np.array([1.0 + 0.0j])
    for value in features:
        angle = np.pi * value
        qubit = np.array([np.cos(angle / 2), np.sin(angle / 2)], dtype=complex)
        state = np.kron(state, qubit)
    return state


def state_overlap_kernel(left, right):
    left_state = product_angle_state(left)
    right_state = product_angle_state(right)
    return float(abs(np.vdot(left_state, right_state)) ** 2)


def classical_product_formula(left, right):
    delta = np.asarray(left, dtype=float) - np.asarray(right, dtype=float)
    return float(np.prod(np.cos(np.pi * delta / 2) ** 2))


pairs = [
    (np.array([0.10, 0.20]), np.array([0.15, 0.25])),
    (np.array([0.10, 0.10]), np.array([0.90, 0.90])),
    (np.array([0.10, 0.90]), np.array([0.90, 0.10])),
]

print("pair quantum_overlap classical_formula absolute_difference")
for index, (left, right) in enumerate(pairs, 1):
    quantum_value = state_overlap_kernel(left, right)
    classical_value = classical_product_formula(left, right)
    difference = abs(quantum_value - classical_value)
    assert np.isclose(quantum_value, classical_value, atol=1e-12)
    print(f"{index:>4} {quantum_value:>15.9f} {classical_value:>17.9f} "
          f"{difference:>19.2e}")

print("conclusion=this feature map has an exact, inexpensive classical kernel formula")
