"""Verify permutation symmetry for a two-qubit model and its readout."""

import numpy as np


def ry(angle):
    return np.array([
        [np.cos(angle / 2), -np.sin(angle / 2)],
        [np.sin(angle / 2), np.cos(angle / 2)],
    ], dtype=complex)


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)
SWAP = np.array([
    [1, 0, 0, 0], [0, 0, 1, 0],
    [0, 1, 0, 0], [0, 0, 0, 1],
], dtype=complex)
SYMMETRIC_READOUT = (np.kron(Z, I) + np.kron(I, Z)) / 2

def exponential_of_hermitian(hermitian):
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    return eigenvectors @ np.diag(np.exp(-1j * eigenvalues)) @ eigenvectors.conj().T


def symmetric_layer(shared_angle, interaction_angle):
    shared_rotation = np.kron(ry(shared_angle), ry(shared_angle))
    interaction = interaction_angle * (
        np.kron(X, X) + np.kron(Y, Y) + np.kron(Z, Z)
    )
    return exponential_of_hermitian(interaction) @ shared_rotation


def encode(features):
    return np.kron(ry(features[0]), ry(features[1])) @ np.array(
        [1.0, 0.0, 0.0, 0.0], dtype=complex
    )


def prediction(features, layer):
    state = layer @ encode(features)
    return float(np.real(np.vdot(state, SYMMETRIC_READOUT @ state)))


layer = symmetric_layer(shared_angle=0.7, interaction_angle=0.3)
commutator_norm = np.linalg.norm(layer @ SWAP - SWAP @ layer)
features = np.array([0.25, 1.10])
original_prediction = prediction(features, layer)
swapped_prediction = prediction(features[::-1], layer)

assert commutator_norm < 1e-12
assert np.isclose(original_prediction, swapped_prediction, atol=1e-12)

print(f"commutator_norm={commutator_norm:.3e}")
print(f"prediction_original={original_prediction:.9f}")
print(f"prediction_after_input_swap={swapped_prediction:.9f}")
print("invariance_verified=True")
print("boundary=the restriction is appropriate only when the target label is swap-invariant")
