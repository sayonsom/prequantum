"""Apply amplitude amplification to a nonuniform prepared state."""

from math import asin, ceil, floor, pi, sin, sqrt

import numpy as np


probabilities = np.array([0.14, 0.14, 0.14, 0.12, 0.14, 0.14, 0.10, 0.08])
prepared = np.sqrt(probabilities).astype(complex)
good = {3, 7}

projector_good = np.zeros((8, 8), dtype=complex)
for index in good:
    projector_good[index, index] = 1.0

phase_mark = np.eye(8) - 2 * projector_good
reflect_prepared = 2 * np.outer(prepared, prepared.conj()) - np.eye(8)
amplification_step = reflect_prepared @ phase_mark

initial_success = float(sum(probabilities[index] for index in good))
theta = asin(sqrt(initial_success))
continuous = pi / (4 * theta) - 0.5
candidates = {0, max(0, floor(continuous)), max(0, ceil(continuous))}
iterations = max(candidates, key=lambda k: sin((2 * k + 1) * theta) ** 2)

state = prepared.copy()
for _ in range(iterations):
    state = amplification_step @ state
final_success = float(sum(abs(state[index]) ** 2 for index in good))

print(f"initial good probability: {initial_success:.3f}")
print("iterations:", iterations)
print(f"final good probability: {final_success:.3f}")

assert np.isclose(np.linalg.norm(prepared), 1.0)
assert np.isclose(final_success, sin((2 * iterations + 1) * theta) ** 2)
assert final_success > 0.95

# In a circuit, reflection about the prepared state is implemented as A S0 A-dagger.
