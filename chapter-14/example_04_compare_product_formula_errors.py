import numpy as np
from scipy.linalg import expm


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

A = -np.kron(Z, Z)
B = -0.5 * (np.kron(X, I) + np.kron(I, X))
H = A + B
total_time = 1.0
exact = expm(-1j * H * total_time)


def first_order(steps):
    dt = total_time / steps
    # Temporal order is A then B; the rightmost matrix acts first.
    step = expm(-1j * B * dt) @ expm(-1j * A * dt)
    return np.linalg.matrix_power(step, steps)


def second_order(steps):
    dt = total_time / steps
    step = (
        expm(-1j * A * dt / 2)
        @ expm(-1j * B * dt)
        @ expm(-1j * A * dt / 2)
    )
    return np.linalg.matrix_power(step, steps)


step_counts = np.array([1, 2, 4, 8, 16, 32, 64])
first_errors = np.array([np.linalg.norm(first_order(n) - exact, ord=2) for n in step_counts])
second_errors = np.array([np.linalg.norm(second_order(n) - exact, ord=2) for n in step_counts])

first_slope = float(np.polyfit(np.log(step_counts[2:]), np.log(first_errors[2:]), 1)[0])
second_slope = float(np.polyfit(np.log(step_counts[2:]), np.log(second_errors[2:]), 1)[0])

assert np.all(np.diff(first_errors) < 0)
assert np.all(np.diff(second_errors) < 0)
assert -1.1 < first_slope < -0.9
assert -2.1 < second_slope < -1.9

print("steps first_order_error second_order_error")
for steps, error_1, error_2 in zip(step_counts, first_errors, second_errors):
    print(f"{steps:5d} {error_1:.10f} {error_2:.10f}")
print(f"fitted_first_order_slope={first_slope:.4f}")
print(f"fitted_second_order_slope={second_slope:.4f}")
print("boundary=these slopes describe this bounded operator-norm experiment, not every Hamiltonian")
