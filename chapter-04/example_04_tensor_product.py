import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
labels = ("00", "01", "10", "11")

def show(name, state):
    visible = {label: complex(np.real_if_close(value))
               for label, value in zip(labels, state) if not np.isclose(value, 0)}
    print(name, state.shape, visible)

definite = np.kron(ket_0, ket_1)
product_superposition = np.kron(ket_plus, ket_0)
bell_phi_plus = (
    np.kron(ket_0, ket_0) + np.kron(ket_1, ket_1)
) / np.sqrt(2)

show("|0> tensor |1>", definite)
show("|+> tensor |0>", product_superposition)
show("Bell Phi-plus", bell_phi_plus)

print(np.linalg.det(product_superposition.reshape(2, 2)))
print(np.linalg.det(bell_phi_plus.reshape(2, 2)))

# |0> tensor |1> (4,) {'01': (1+0j)}
# |+> tensor |0> (4,) {'00': (0.7071067811865475+0j), '10': (0.7071067811865475+0j)}
# Bell Phi-plus (4,) {'00': (0.7071067811865475+0j), '11': (0.7071067811865475+0j)}
# 0j
# (0.4999999999999999+0j)
