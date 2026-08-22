import numpy as np


def left_probabilities(state: np.ndarray) -> np.ndarray:
    probabilities = np.abs(state) ** 2
    return np.array([probabilities[:2].sum(), probabilities[2:].sum()])


def measure_left(state: np.ndarray, seed: int) -> tuple[int, np.ndarray]:
    rng = np.random.default_rng(seed)
    local = left_probabilities(state)
    result = int(rng.choice([0, 1], p=local))
    conditioned = state.copy()
    conditioned[2:] = 0 if result == 0 else conditioned[2:]
    conditioned[:2] = conditioned[:2] if result == 0 else 0
    conditioned /= np.linalg.norm(conditioned)
    return result, conditioned


bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
I = np.eye(2, dtype=complex)
right_flipped = np.kron(I, X) @ bell

print("left probabilities before:", left_probabilities(bell))
print("left probabilities after right X:", left_probabilities(right_flipped))

result, conditioned = measure_left(bell, seed=7)
print("measured left:", result)
print("conditioned joint state:", np.real_if_close(np.round(conditioned, 4)))

# left probabilities before: [0.5 0.5]
# left probabilities after right X: [0.5 0.5]
# measured left: 1
# conditioned joint state: [0. 0. 0. 1.]
