import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
shrink = np.array([[1, 0], [0, 0.5]], dtype=complex)

def is_unitary(operator, tolerance=1e-10):
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        return False
    identity = np.eye(operator.shape[0], dtype=complex)
    return np.allclose(operator.conj().T @ operator, identity, atol=tolerance)

for name, operator in (("H", H), ("X", X), ("shrink", shrink)):
    print(name, is_unitary(operator))

test_state = np.array([1, 0], dtype=complex)
print(np.linalg.norm(test_state), np.linalg.norm(shrink @ test_state))
print(np.round(np.real_if_close(shrink.conj().T @ shrink), 4))

# H True
# X True
# shrink False
# 1.0 1.0
# [[1.   0.  ]
#  [0.   0.25]]
