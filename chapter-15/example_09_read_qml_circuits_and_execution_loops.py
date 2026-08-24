"""Read kernel and variational QML circuits as parts of classical algorithms."""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import SparsePauliOp, Statevector


Z_ON_Q0 = SparsePauliOp.from_list([("IZ", 1.0)])


def feature_map(features):
    """Return F(x), where feature j controls one RY(pi*x_j) gate."""
    features = np.asarray(features, dtype=float)
    if features.shape != (2,) or not np.all(np.isfinite(features)):
        raise ValueError("features must contain two finite values")
    circuit = QuantumCircuit(2, name="F(x)")
    for qubit, value in enumerate(features):
        circuit.ry(np.pi * value, qubit)
    return circuit


def kernel_circuit(left, right):
    """Prepare F(right)^dagger F(left)|00> for an overlap measurement."""
    circuit = QuantumCircuit(2, name="kernel")
    circuit.compose(feature_map(left), inplace=True)
    circuit.compose(feature_map(right).inverse(), inplace=True)
    return circuit


def all_zero_probability(circuit):
    probabilities = Statevector.from_instruction(circuit).probabilities_dict()
    return float(probabilities.get("00", 0.0))


def classical_product_kernel(left, right):
    delta = np.asarray(left, dtype=float) - np.asarray(right, dtype=float)
    return float(np.prod(np.cos(np.pi * delta / 2) ** 2))


def variational_circuit(features, parameters):
    """Build F(x), a trainable-entangling block, and a final trainable layer."""
    parameters = np.asarray(parameters, dtype=float)
    if parameters.shape != (4,) or not np.all(np.isfinite(parameters)):
        raise ValueError("parameters must contain four finite values")
    circuit = feature_map(features)
    circuit.name = "variational_model"
    circuit.ry(parameters[0], 0)
    circuit.ry(parameters[1], 1)
    circuit.cx(0, 1)
    circuit.ry(parameters[2], 0)
    circuit.ry(parameters[3], 1)
    return circuit


def prediction(features, parameters):
    state = Statevector.from_instruction(variational_circuit(features, parameters))
    return float(np.real(state.expectation_value(Z_ON_Q0)))


def parameter_shift_derivative(features, parameters, parameter_index):
    plus = np.asarray(parameters, dtype=float).copy()
    minus = np.asarray(parameters, dtype=float).copy()
    plus[parameter_index] += np.pi / 2
    minus[parameter_index] -= np.pi / 2
    return 0.5 * (prediction(features, plus) - prediction(features, minus))


left = np.array([0.10, 0.70])
right = np.array([0.35, 0.20])
logical_kernel = kernel_circuit(left, right)
measured_overlap = all_zero_probability(logical_kernel)
classical_overlap = classical_product_kernel(left, right)
assert np.isclose(measured_overlap, classical_overlap, atol=1e-12)

features = np.array([0.20, 0.60])
parameters = np.array([0.30, -0.40, 0.25, 0.10])
logical_model = variational_circuit(features, parameters)
logical_prediction = prediction(features, parameters)

compiled_model = transpile(
    logical_model,
    basis_gates=["rz", "sx", "x", "cx"],
    coupling_map=[[0, 1], [1, 0]],
    optimization_level=1,
    seed_transpiler=17,
)
compiled_state = Statevector.from_instruction(compiled_model)
compiled_prediction = float(np.real(compiled_state.expectation_value(Z_ON_Q0)))
assert np.isclose(logical_prediction, compiled_prediction, atol=1e-12)

shift_derivative = parameter_shift_derivative(features, parameters, 2)
epsilon = 1e-6
finite_difference_parameters = parameters.copy()
finite_difference_parameters[2] += epsilon
plus_value = prediction(features, finite_difference_parameters)
finite_difference_parameters[2] -= 2 * epsilon
minus_value = prediction(features, finite_difference_parameters)
finite_difference = (plus_value - minus_value) / (2 * epsilon)
assert np.isclose(shift_derivative, finite_difference, atol=1e-9)

parameter_count = len(parameters)
batch_size = 5
predictions_per_sample = 1 + 2 * parameter_count
evaluations_per_gradient_step = batch_size * predictions_per_sample

print(f"kernel_all_zero_probability={measured_overlap:.9f}")
print(f"kernel_classical_formula={classical_overlap:.9f}")
print(f"logical_prediction={logical_prediction:.9f}")
print(f"compiled_prediction={compiled_prediction:.9f}")
print(f"logical_operations={dict(logical_model.count_ops())}")
print(f"compiled_operations={dict(compiled_model.count_ops())}")
print(f"parameter_shift_derivative={shift_derivative:.9f}")
print(f"finite_difference_check={finite_difference:.9f}")
print(f"naive_exact_evaluations_per_gradient_step={evaluations_per_gradient_step}")
print("boundary=labels, loss, optimizer, shots, and target selection remain outside "
      "the logical circuit")
