import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)

after_first_h = H @ ket_0
after_t = T @ after_first_h
final_state = H @ after_t
probabilities = np.abs(final_state) ** 2

print(np.round(after_first_h, 4))
print(np.round(after_t, 4))
print(np.round(final_state, 4))
print(np.round(probabilities, 4))
print(np.isclose(probabilities.sum(), 1.0))

# [0.7071+0.j 0.7071+0.j]
# [0.7071+0.j  0.5   +0.5j]
# [0.8536+0.3536j 0.1464-0.3536j]
# [0.8536 0.1464]
# True
