"""Validate angle and amplitude encoding records, including basis order."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def angle_state_numpy(features):
    """Match Qiskit's statevector order |q_(n-1)...q_0>."""
    features = np.asarray(features, dtype=float)
    if features.ndim != 1 or not np.all(np.isfinite(features)):
        raise ValueError("features must be a finite one-dimensional array")
    if np.any((features < 0.0) | (features > 1.0)):
        raise ValueError("this example expects features scaled to [0, 1]")
    state = np.array([1.0 + 0.0j])
    for value in features[::-1]:
        angle = np.pi * value
        state = np.kron(
            state,
            np.array([np.cos(angle / 2), np.sin(angle / 2)], dtype=complex),
        )
    return state


def angle_state_qiskit(features):
    features = np.asarray(features, dtype=float)
    circuit = QuantumCircuit(len(features))
    for qubit, value in enumerate(features):
        circuit.ry(np.pi * value, qubit)
    return Statevector.from_instruction(circuit).data


def amplitude_state(values):
    values = np.asarray(values, dtype=complex)
    if values.ndim != 1 or not np.all(np.isfinite(values)):
        raise ValueError("values must be a finite one-dimensional array")
    if values.size == 0:
        raise ValueError("values must not be empty")
    dimension = 1 << max(1, (values.size - 1).bit_length())
    padded = np.zeros(dimension, dtype=complex)
    padded[: values.size] = values
    norm = np.linalg.norm(padded)
    if norm <= 1e-12:
        raise ValueError("the zero vector cannot define an amplitude state")
    return padded / norm


features = np.array([0.20, 0.65, 0.40])
numpy_state = angle_state_numpy(features)
qiskit_state = angle_state_qiskit(features)
assert np.allclose(numpy_state, qiskit_state, atol=1e-12)

values = np.array([1.0, 2.0, 3.0])
amplitudes = amplitude_state(values)
scaled_amplitudes = amplitude_state(2.0 * values)
assert np.isclose(np.linalg.norm(amplitudes), 1.0, atol=1e-12)
assert np.allclose(amplitudes, scaled_amplitudes, atol=1e-12)

print(f"angle_features={features.tolist()}")
print(f"qiskit_basis_order=|q2 q1 q0>, state_dimension={numpy_state.size}")
print(f"numpy_matches_qiskit={np.allclose(numpy_state, qiskit_state)}")
print(f"amplitude_input_length={values.size}, padded_dimension={amplitudes.size}")
print(f"amplitude_norm={np.linalg.norm(amplitudes):.12f}")
print("scale_information_preserved=False; x and 2*x encode the same normalized state")
