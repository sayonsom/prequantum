"""Trace the four conditional branches in the teleportation identity."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
one = np.array([0.0, 1.0], dtype=complex)
i2 = np.eye(2, dtype=complex)
h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
x = np.array([[0, 1], [1, 0]], dtype=complex)
z = np.array([[1, 0], [0, -1]], dtype=complex)

theta, phi = 1.1, 0.7
psi = np.array(
    [np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)],
    dtype=complex,
)
bell = (np.kron(zero, zero) + np.kron(one, one)) / np.sqrt(2)
state = np.kron(psi, bell)  # Tensor order: Alice message, Alice ebit, Bob ebit.

cnot_01 = np.zeros((8, 8), dtype=complex)
for q0 in (0, 1):
    for q1 in (0, 1):
        for q2 in (0, 1):
            source = 4 * q0 + 2 * q1 + q2
            target = 4 * q0 + 2 * (q1 ^ q0) + q2
            cnot_01[target, source] = 1

state = np.kron(np.kron(h, i2), i2) @ cnot_01 @ state

expected = {
    "00": (psi, i2),
    "01": (x @ psi, x),
    "10": (z @ psi, z),
    "11": (x @ z @ psi, z @ x),
}

for outcome, (expected_bob, correction) in expected.items():
    start = int(outcome, 2) * 2
    branch = state[start : start + 2]
    probability = float(np.vdot(branch, branch).real)
    bob = branch / np.sqrt(probability)
    corrected = correction @ bob
    fidelity = abs(np.vdot(psi, corrected)) ** 2
    print(
        f"outcome={outcome} probability={probability:.3f} "
        f"branch_ok={np.allclose(bob, expected_bob)} "
        f"corrected_fidelity={fidelity:.6f}"
    )
    assert np.isclose(probability, 0.25)
    assert np.allclose(bob, expected_bob)
    assert np.isclose(fidelity, 1.0)
