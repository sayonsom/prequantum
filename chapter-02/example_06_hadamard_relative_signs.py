import numpy as np

H = np.array(
    [[1, 1],
     [1, -1]],
    dtype=complex,
) / np.sqrt(2)

same_sign = np.array([1, 1], dtype=complex) / np.sqrt(2)
opposite_sign = np.array([1, -1], dtype=complex) / np.sqrt(2)

print(np.abs(same_sign) ** 2)
print(np.abs(opposite_sign) ** 2)
print(np.round(H @ same_sign, 4))
print(np.round(H @ opposite_sign, 4))
# [0.5 0.5]
# [0.5 0.5]
# [1.+0.j 0.+0.j]
# [0.+0.j 1.+0.j]
