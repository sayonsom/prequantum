import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
psi = np.array([1 + 2j, -2], dtype=complex) / 3

bra_as_row = psi.conj()[None, :]
ket_as_column = psi[:, None]

print(psi.shape, ket_as_column.shape, bra_as_row.shape)
print(np.round(bra_as_row, 4))
print(np.round(np.vdot(psi, psi), 4))

p0 = abs(np.vdot(ket_0, psi)) ** 2
p1 = abs(np.vdot(ket_1, psi)) ** 2
print(np.round([p0, p1], 4))
print(np.isclose(p0 + p1, 1.0))

# (2,) (2, 1) (1, 2)
# [[ 0.3333-0.6667j -0.6667-0.j    ]]
# (1+0j)
# [0.5556 0.4444]
# True
