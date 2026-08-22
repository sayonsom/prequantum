"""Verify circuit-matrix decompositions of Pauli evolution blocks."""

import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
HADAMARD = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
CNOT = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=complex,
)


def rz(angle: float) -> np.ndarray:
    return np.diag([np.exp(-1j * angle / 2), np.exp(1j * angle / 2)])


def rx(angle: float) -> np.ndarray:
    return np.cos(angle / 2) * I - 1j * np.sin(angle / 2) * X


def exp_zz(theta: float) -> np.ndarray:
    return CNOT @ np.kron(I, rz(2 * theta)) @ CNOT


def exp_xx(theta: float) -> np.ndarray:
    basis_change = np.kron(HADAMARD, HADAMARD)
    return basis_change @ exp_zz(theta) @ basis_change


theta = 0.3
checks = {
    "exp(-i theta ZZ)": np.allclose(
        exp_zz(theta), expm(-1j * theta * np.kron(Z, Z)), atol=1e-12
    ),
    "exp(-i theta XX)": np.allclose(
        exp_xx(theta), expm(-1j * theta * np.kron(X, X)), atol=1e-12
    ),
    "exp(-i theta XI)": np.allclose(
        np.kron(rx(2 * theta), I),
        expm(-1j * theta * np.kron(X, I)),
        atol=1e-12,
    ),
}

for label, passed in checks.items():
    print(f"{label}: {passed}")
assert all(checks.values())

