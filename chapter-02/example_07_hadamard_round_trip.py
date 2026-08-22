import numpy as np

H = np.array(
    [[1, 1],
     [1, -1]],
    dtype=complex,
) / np.sqrt(2)

start = np.array([0.6, 0.8], dtype=complex)
after_one = H @ start
after_two = H @ after_one

print(np.round(after_one, 4))
print(np.round(after_two, 4))
print(np.allclose(after_two, start))
# [ 0.9899+0.j -0.1414+0.j]
# [0.6+0.j 0.8+0.j]
# True
