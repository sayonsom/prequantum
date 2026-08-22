import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)

projector_0 = np.outer(ket_0, ket_0.conj())
transition_01 = np.outer(ket_0, ket_1.conj())

probability_from_inner = abs(np.vdot(ket_0, ket_plus)) ** 2
probability_from_projector = np.vdot(
    ket_plus, projector_0 @ ket_plus
).real

print(projector_0)
print(np.round(probability_from_inner, 4))
print(np.round(probability_from_projector, 4))
print(np.allclose(projector_0 @ projector_0, projector_0))
print(transition_01 @ ket_1)
print(np.allclose(transition_01 @ transition_01, transition_01))

# [[1.+0.j 0.+0.j]
#  [0.+0.j 0.+0.j]]
# 0.5
# 0.5
# True
# [1.+0.j 0.+0.j]
# False
