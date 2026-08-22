"""Compare first- and second-order product formulas with exact evolution."""

import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

A = np.kron(Z, Z)
B = 0.7 * (np.kron(X, I) + np.kron(I, X))
H = A + B
total_time = 1.0
exact = expm(-1j * H * total_time)


def repeat_step(step: np.ndarray, repetitions: int) -> np.ndarray:
    result = np.eye(step.shape[0], dtype=complex)
    for _ in range(repetitions):
        result = step @ result
    return result


def first_order(repetitions: int) -> np.ndarray:
    dt = total_time / repetitions
    step = expm(-1j * A * dt) @ expm(-1j * B * dt)
    return repeat_step(step, repetitions)


def second_order(repetitions: int) -> np.ndarray:
    dt = total_time / repetitions
    step = (
        expm(-1j * A * dt / 2)
        @ expm(-1j * B * dt)
        @ expm(-1j * A * dt / 2)
    )
    return repeat_step(step, repetitions)


print("steps   first-order error   second-order error")
for steps in [1, 2, 4, 8, 16, 32]:
    error_1 = np.linalg.norm(first_order(steps) - exact, ord=2)
    error_2 = np.linalg.norm(second_order(steps) - exact, ord=2)
    print(f"{steps:5d}   {error_1:17.9f}   {error_2:18.9f}")

