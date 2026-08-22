import numpy as np

def phase(theta):
    return np.diag([1, np.exp(1j * theta)]).astype(complex)

def rz(theta):
    return np.diag([
        np.exp(-1j * theta / 2),
        np.exp(1j * theta / 2),
    ]).astype(complex)

theta = np.pi / 3
P = phase(theta)
RZ = rz(theta)
print("P = exp(i theta/2) Rz:",
      np.allclose(P, np.exp(1j * theta / 2) * RZ))

T = phase(np.pi / 4)
S = phase(np.pi / 2)
Z = phase(np.pi)
print("T squared is S:", np.allclose(T @ T, S))
print("S squared is Z:", np.allclose(S @ S, Z))

controlled_p = np.diag([1, 1, 1, np.exp(1j * theta)])
controlled_rz = np.diag([
    1, 1, np.exp(-1j * theta / 2), np.exp(1j * theta / 2)
])
relative = controlled_p @ controlled_rz.conj().T
print("Controlled ratio is one global phase:",
      np.allclose(relative, relative[0, 0] * np.eye(4)))

# P = exp(i theta/2) Rz: True
# T squared is S: True
# S squared is Z: True
# Controlled ratio is one global phase: False
