import numpy as np


def qft_matrix(size):
    omega = np.exp(2j * np.pi / size)
    return np.array(
        [[omega ** (row * column) / np.sqrt(size) for column in range(size)]
         for row in range(size)],
        dtype=complex,
    )


size = 8
period = 2
qft = qft_matrix(size)
assert np.allclose(qft.conj().T @ qft, np.eye(size))

# The nonzero labels differ by the declared period: 0, 2, 4, and 6.
periodic_state = np.zeros(size, dtype=complex)
periodic_state[::period] = 1 / np.sqrt(size // period)
transformed_state = qft @ periodic_state
probabilities = np.abs(transformed_state) ** 2
peak_labels = np.flatnonzero(probabilities > 1e-10).tolist()

assert peak_labels == [0, 4]
assert np.allclose(probabilities[peak_labels], [0.5, 0.5])
assert np.isclose(probabilities.sum(), 1.0)

rng = np.random.default_rng(12)
samples = rng.choice(size, size=12, p=probabilities).tolist()
assert set(samples).issubset({0, 4})

print(f"input_nonzero_labels={np.flatnonzero(periodic_state).tolist()}")
print(f"qft_peak_labels={peak_labels}")
print(f"measurement_probabilities={np.round(probabilities, 3).tolist()}")
print(f"twelve_measurements={samples}")
print("interface_note=measurement samples labels; it does not return every complex amplitude")
