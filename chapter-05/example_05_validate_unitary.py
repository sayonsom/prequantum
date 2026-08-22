import numpy as np

def is_unitary(candidate, atol=1e-10):
    matrix = np.asarray(candidate, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] == 0:
        return False
    if matrix.shape[0] != matrix.shape[1]:
        return False
    if not np.isfinite(matrix).all():
        return False
    identity = np.eye(matrix.shape[0], dtype=complex)
    return np.allclose(matrix.conj().T @ matrix, identity,
                       atol=atol, rtol=0.0)

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
rotation = np.array([[0.6, 0.8], [-0.8, 0.6]], dtype=complex)
shear = np.array([[1, 1], [0, 1]], dtype=complex)

print("H:", is_unitary(H))
print("real rotation:", is_unitary(rotation))
print("shear:", is_unitary(shear))
print("rectangular:", is_unitary([[1, 0, 0], [0, 1, 0]]))
print("non-finite:", is_unitary([[1, 0], [0, np.nan]]))

state = np.array([0.6, 0.8j], dtype=complex)
print("norm preserved:",
      np.isclose(np.vdot(H @ state, H @ state), np.vdot(state, state)))

# H: True
# real rotation: True
# shear: False
# rectangular: False
# non-finite: False
# norm preserved: True
