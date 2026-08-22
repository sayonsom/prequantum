import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

print("H|0> = |+>:", np.allclose(H @ ket_0, ket_plus))
print("H|-> = |1>:", np.allclose(H @ ket_minus, ket_1))
print("H squared is I:", np.allclose(H @ H, np.eye(2)))

x_then_h = H @ X @ ket_0
h_then_x = X @ H @ ket_0
print("X then H gives |->:", np.allclose(x_then_h, ket_minus))
print("H then X gives |+>:", np.allclose(h_then_x, ket_plus))
print("The two sequences match:", np.allclose(x_then_h, h_then_x))
print("H Z H is X:", np.allclose(H @ Z @ H, X))

# H|0> = |+>: True
# H|-> = |1>: True
# H squared is I: True
# X then H gives |->: True
# H then X gives |+>: True
# The two sequences match: False
# H Z H is X: True
