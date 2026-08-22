import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
I = np.eye(2, dtype=complex)
CNOT = np.array(
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 0, 1],
     [0, 0, 1, 0]],
    dtype=complex,
)

print(np.round(np.real_if_close(H @ X @ ket_0), 4))

state_00 = np.kron(ket_0, ket_0)
after_h = np.kron(H, I) @ state_00
after_cnot = CNOT @ after_h

print(np.round(np.real_if_close(state_00), 4))
print(np.round(np.real_if_close(after_h), 4))
print(np.round(np.real_if_close(after_cnot), 4))

# [ 0.7071 -0.7071]
# [1. 0. 0. 0.]
# [0.7071 0.     0.7071 0.    ]
# [0.7071 0.     0.     0.7071]
