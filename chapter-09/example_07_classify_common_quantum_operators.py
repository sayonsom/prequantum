"""Classify matrices as Hermitian, unitary, and projective."""

import numpy as np


i2 = np.eye(2, dtype=complex)
x = np.array([[0, 1], [1, 0]], dtype=complex)
h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
phase = np.array([[1, 0], [0, 1j]], dtype=complex)
p_zero = np.array([[1, 0], [0, 0]], dtype=complex)

operators = {"X": x, "H": h, "S": phase, "|0><0|": p_zero}

def classify(operator):
    return {
        "Hermitian": np.allclose(operator, operator.conj().T),
        "unitary": np.allclose(operator.conj().T @ operator, i2),
        "projector": np.allclose(operator @ operator, operator),
    }


results = {name: classify(operator) for name, operator in operators.items()}
for name, result in results.items():
    print(f"{name:7s} {result}")

assert results["X"] == {"Hermitian": True, "unitary": True, "projector": False}
assert results["H"] == {"Hermitian": True, "unitary": True, "projector": False}
assert results["S"] == {"Hermitian": False, "unitary": True, "projector": False}
assert results["|0><0|"] == {
    "Hermitian": True,
    "unitary": False,
    "projector": True,
}
