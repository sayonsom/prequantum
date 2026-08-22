from collections import Counter

import numpy as np


class QubitState:
    """A teaching model for one normalized state and standard-basis measurement."""

    def __init__(self, values):
        state = np.asarray(values, dtype=complex)
        if state.shape != (2,):
            raise ValueError("A one-qubit state must contain exactly two amplitudes.")
        if not np.all(np.isfinite(state)):
            raise ValueError("Amplitudes must be finite.")
        norm = np.linalg.norm(state)
        if np.isclose(norm, 0.0):
            raise ValueError("The zero vector cannot be normalized.")
        self.state = state / norm

    def probabilities(self):
        probabilities = np.abs(self.state) ** 2
        if not np.isclose(np.sum(probabilities), 1.0):
            raise RuntimeError("The stored state is not normalized.")
        return probabilities

    def measure(self, rng):
        probabilities = self.probabilities()
        outcome = int(rng.choice([0, 1], p=probabilities))
        self.state = np.array(
            [1, 0] if outcome == 0 else [0, 1],
            dtype=complex,
        )
        return outcome


single = QubitState([0.6, 0.8])
single_outcome = single.measure(np.random.default_rng(7))
print(single_outcome)
print(single.state)

rng = np.random.default_rng(42)
fresh_outcomes = [QubitState([0.6, 0.8]).measure(rng) for _ in range(1000)]
print(Counter(fresh_outcomes))
# 1
# [0.+0.j 1.+0.j]
# Counter({1: 638, 0: 362})
