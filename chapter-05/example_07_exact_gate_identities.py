import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
S = np.diag([1, 1j]).astype(complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I = np.eye(2, dtype=complex)

print("T squared is exactly S:", np.allclose(T @ T, S))
print("T to the fourth is exactly Z:",
      np.allclose(np.linalg.matrix_power(T, 4), Z))
print("H T^4 H is exactly X:",
      np.allclose(H @ np.linalg.matrix_power(T, 4) @ H, X))
print("T dagger equals T^7:",
      np.allclose(T.conj().T, np.linalg.matrix_power(T, 7)))
print("T^8 is identity:",
      np.allclose(np.linalg.matrix_power(T, 8), I))

# T squared is exactly S: True
# T to the fourth is exactly Z: True
# H T^4 H is exactly X: True
# T dagger equals T^7: True
# T^8 is identity: True
