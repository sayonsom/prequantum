"""Example 16.5: deterministic p=1 QAOA statevector experiment."""

from itertools import product

import numpy as np


linear = np.array([-47.0, -76.0, -82.0])
quadratic = np.array(
    [
        [0.0, 40.0, 60.0],
        [0.0, 0.0, 120.0],
        [0.0, 0.0, 0.0],
    ]
)
constant = 90.0
n_qubits = linear.size
dimension = 2**n_qubits

bitstrings = list(product((0, 1), repeat=n_qubits))
raw_cost = np.array(
    [
        constant
        + linear @ np.asarray(bits, dtype=float)
        + np.asarray(bits, dtype=float) @ quadratic @ np.asarray(bits, dtype=float)
        for bits in bitstrings
    ],
    dtype=float,
)

# An affine rescaling preserves cost ordering. It only changes the useful gamma
# scale; both the original and scaled objectives are recorded.
scaled_cost = (raw_cost - raw_cost.min()) / (raw_cost.max() - raw_cost.min())


def apply_x_mixer(state, beta):
    state = state.copy()
    for qubit in range(n_qubits):
        next_state = np.empty_like(state)
        cosine = np.cos(beta)
        sine = np.sin(beta)
        for basis_index in range(dimension):
            partner = basis_index ^ (1 << qubit)
            next_state[basis_index] = (
                cosine * state[basis_index]
                - 1j * sine * state[partner]
            )
        state = next_state
    return state


def qaoa_probabilities(gamma, beta):
    state = np.ones(dimension, dtype=complex) / np.sqrt(dimension)
    state *= np.exp(-1j * gamma * scaled_cost)
    state = apply_x_mixer(state, beta)
    probabilities = np.abs(state) ** 2
    assert np.isclose(probabilities.sum(), 1.0, atol=1e-12)
    return probabilities


best = None
for gamma in np.linspace(0.0, 2.0 * np.pi, 181, endpoint=False):
    for beta in np.linspace(0.0, np.pi / 2.0, 121):
        probabilities = qaoa_probabilities(gamma, beta)
        expectation = float(probabilities @ raw_cost)
        candidate = (expectation, gamma, beta, probabilities)
        if best is None or expectation < best[0]:
            best = candidate

expectation, gamma, beta, probabilities = best
order = np.argsort(-probabilities, kind="stable")

print(f"gamma={gamma:.6f}")
print(f"beta={beta:.6f}")
print(f"expected_raw_cost={expectation:.6f}")
for index in order[:4]:
    bits = "".join(str(bit) for bit in bitstrings[index])
    print(
        f"bits={bits}, raw_cost={raw_cost[index]:.1f}, "
        f"probability={probabilities[index]:.6f}"
    )

