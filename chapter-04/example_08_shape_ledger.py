import numpy as np

psi = np.array([1, 1j], dtype=complex) / np.sqrt(2)
ket_0 = np.array([1, 0], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)

column = psi[:, None]
bra = psi.conj()[None, :]
inner_matrix = bra @ column
outer_matrix = column @ bra
joint_state = np.kron(psi, ket_0)
lifted_h = np.kron(H, I)

print("ket storage", psi.shape)
print("column", column.shape)
print("bra", bra.shape)
print("inner", inner_matrix.shape, np.round(inner_matrix[0, 0], 4))
print("outer", outer_matrix.shape)
print("joint", joint_state.shape)
print("lifted operator", lifted_h.shape)
print("transformed joint", (lifted_h @ joint_state).shape)

# ket storage (2,)
# column (2, 1)
# bra (1, 2)
# inner (1, 1) (1+0j)
# outer (2, 2)
# joint (4,)
# lifted operator (4, 4)
# transformed joint (4,)
