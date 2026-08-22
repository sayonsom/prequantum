import numpy as np

def rz(theta):
    return np.diag([
        np.exp(-1j * theta / 2),
        np.exp(1j * theta / 2),
    ]).astype(complex)

def equal_up_to_global_phase(actual, expected, atol=1e-10):
    overlap = np.vdot(expected.ravel(), actual.ravel())
    if np.isclose(abs(overlap), 0.0, atol=atol):
        return False
    phase = overlap / abs(overlap)
    return np.allclose(actual, phase * expected, atol=atol, rtol=0.0)

SX = np.array([
    [0.5 + 0.5j, 0.5 - 0.5j],
    [0.5 - 0.5j, 0.5 + 0.5j],
], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

print("SX squared is X:", np.allclose(SX @ SX, X))
H_from_target = rz(np.pi / 2) @ SX @ rz(np.pi / 2)
print("Rz SX Rz equals H up to global phase:",
      equal_up_to_global_phase(H_from_target, H))

CZ = np.diag([1, 1, 1, -1]).astype(complex)
I = np.eye(2, dtype=complex)
target_h = np.kron(I, H)
CNOT_from_CZ = target_h @ CZ @ target_h
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
], dtype=complex)
print("H-on-target, CZ, H-on-target equals CNOT:",
      np.allclose(CNOT_from_CZ, CNOT))

# SX squared is X: True
# Rz SX Rz equals H up to global phase: True
# H-on-target, CZ, H-on-target equals CNOT: True
