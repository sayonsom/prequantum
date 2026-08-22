import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
x = np.array([[0, 1], [1, 0]], dtype=complex)
z = np.array([[1, 0], [0, -1]], dtype=complex)

plus = h @ zero


def probabilities(state, basis_change):
    amplitudes = basis_change @ state
    return np.abs(amplitudes) ** 2


states = {
    "no error": plus,
    "X after preparation": x @ plus,
    "Z after preparation": z @ plus,
}

for label, state in states.items():
    z_basis = probabilities(state, np.eye(2))
    x_basis = probabilities(state, h)
    print(f"{label:20s} Z-basis={z_basis} X-basis={x_basis}")

assert np.allclose(
    probabilities(plus, np.eye(2)),
    probabilities(z @ plus, np.eye(2)),
)
assert np.allclose(probabilities(z @ plus, h), [0.0, 1.0])
