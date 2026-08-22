import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
global_variant = 1j * ket_plus
ket_minus = (ket_0 - ket_1) / np.sqrt(2)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

def probabilities(state):
    return np.abs(state) ** 2

for name, state in (
    ("plus", ket_plus),
    ("i times plus", global_variant),
    ("minus", ket_minus),
):
    print(name, np.round(probabilities(state), 4),
          np.round(probabilities(H @ state), 4))

print(np.isclose(abs(np.vdot(ket_plus, global_variant)) ** 2, 1.0))
print(np.isclose(abs(np.vdot(ket_plus, ket_minus)) ** 2, 0.0))

# plus [0.5 0.5] [1. 0.]
# i times plus [0.5 0.5] [1. 0.]
# minus [0.5 0.5] [0. 1.]
# True
# True
