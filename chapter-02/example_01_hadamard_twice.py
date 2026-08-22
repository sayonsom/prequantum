import numpy as np

H = np.array(
    [[1, 1],
     [1, -1]],
    dtype=complex,
) / np.sqrt(2)

start = np.array([1, 0], dtype=complex)
after_one = H @ start
after_two = H @ after_one

print(np.round(after_one, 4))
print(np.round(after_two, 4))
print(np.allclose(after_two, start))
# [0.7071+0.j 0.7071+0.j]
# [1.+0.j 0.+0.j]
# True
