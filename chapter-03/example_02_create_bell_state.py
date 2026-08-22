import numpy as np


H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)

state = np.array([1, 0, 0, 0], dtype=complex)
after_h = np.kron(H, I) @ state
bell = CNOT @ after_h

print("after H:", np.real_if_close(np.round(after_h, 4)))
print("after CNOT:", np.real_if_close(np.round(bell, 4)))
print("probabilities:", np.round(np.abs(bell) ** 2, 4))

# after H: [0.7071 0.     0.7071 0.    ]
# after CNOT: [0.7071 0.     0.     0.7071]
# probabilities: [0.5 0.  0.  0.5]
