import numpy as np


def normalize_state(values):
    state = np.asarray(values, dtype=complex)
    if state.shape != (2,):
        raise ValueError("A one-qubit state must contain exactly two amplitudes.")
    if not np.all(np.isfinite(state)):
        raise ValueError("Amplitudes must be finite.")

    norm = np.linalg.norm(state)
    if np.isclose(norm, 0.0):
        raise ValueError("The zero vector cannot be normalized.")
    return state / norm


state = normalize_state([3, 4])
probabilities = np.abs(state) ** 2
print(state)
print(probabilities)
print(np.allclose(np.sum(probabilities), 1.0))
# [0.6+0.j 0.8+0.j]
# [0.36 0.64]
# True
