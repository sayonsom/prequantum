import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I = np.eye(2, dtype=complex)

print("X|0> = |1>:", np.allclose(X @ ket_0, ket_1))
print("Z|+> = |->:", np.allclose(Z @ ket_plus, ket_minus))
print("Y|+> = -i|->:", np.allclose(Y @ ket_plus, -1j * ket_minus))

for name, gate in (("X", X), ("Y", Y), ("Z", Z)):
    print(name, "squared is I:", np.allclose(gate @ gate, I))

# X|0> = |1>: True
# Z|+> = |->: True
# Y|+> = -i|->: True
# X squared is I: True
# Y squared is I: True
# Z squared is I: True
