"""Train a bounded one-qubit re-uploading model with parameter-shift gradients."""

import numpy as np
from scipy.optimize import minimize


Z = np.diag([1.0, -1.0]).astype(complex)


def ry(angle):
    return np.array([
        [np.cos(angle / 2), -np.sin(angle / 2)],
        [np.sin(angle / 2), np.cos(angle / 2)],
    ], dtype=complex)


def rz(angle):
    return np.diag([np.exp(-0.5j * angle), np.exp(0.5j * angle)])


def model(input_value, parameters):
    state = np.array([1.0, 0.0], dtype=complex)
    for layer in range(len(parameters) // 2):
        state = ry(input_value) @ state
        state = rz(parameters[2 * layer]) @ state
        state = ry(parameters[2 * layer + 1]) @ state
    return float(np.real(np.vdot(state, Z @ state)))


def predict(inputs, parameters):
    return np.array([model(value, parameters) for value in inputs])


def mean_squared_error(parameters, inputs, targets):
    residuals = predict(inputs, parameters) - targets
    return float(np.mean(residuals**2))


def parameter_shift_gradient(parameters, inputs, targets):
    predictions = predict(inputs, parameters)
    gradient = np.empty_like(parameters)
    for index in range(len(parameters)):
        plus = parameters.copy()
        minus = parameters.copy()
        plus[index] += np.pi / 2
        minus[index] -= np.pi / 2
        prediction_derivative = 0.5 * (predict(inputs, plus) - predict(inputs, minus))
        gradient[index] = 2.0 * np.mean(
            (predictions - targets) * prediction_derivative
        )
    return gradient


target_function = lambda values: 0.65 * np.cos(2 * values) + 0.20 * np.sin(values)
train_inputs = np.linspace(-np.pi, np.pi, 17, endpoint=False)
test_inputs = train_inputs + np.pi / 17
train_targets = target_function(train_inputs)
test_targets = target_function(test_inputs)

rng = np.random.default_rng(12)
initial_parameters = rng.normal(0.0, 0.2, size=6)
result = minimize(
    mean_squared_error,
    initial_parameters,
    args=(train_inputs, train_targets),
    jac=parameter_shift_gradient,
    method="L-BFGS-B",
    options={"maxiter": 500, "gtol": 1e-10},
)

train_error = mean_squared_error(result.x, train_inputs, train_targets)
test_error = mean_squared_error(result.x, test_inputs, test_targets)
assert result.success
assert train_error < 2e-4 and test_error < 2e-4

print(f"optimizer_converged={result.success}, iterations={result.nit}")
print(f"train_mse={train_error:.9f}")
print(f"test_mse={test_error:.9f}")
print(f"parameters={np.round(result.x, 3)}")
print("evidence=exact statevector training on one bounded synthetic regression task")
