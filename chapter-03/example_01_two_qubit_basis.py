import numpy as np


labels = ("00", "01", "10", "11")
left_zero = np.array([1, 0], dtype=complex)
right_one = np.array([0, 1], dtype=complex)

state = np.kron(left_zero, right_one)

print(np.real_if_close(state))
for index, label in enumerate(labels):
    probability = float(abs(state[index]) ** 2)
    print(index, label, probability)

# [0. 1. 0. 0.]
# 0 00 0.0
# 1 01 1.0
# 2 10 0.0
# 3 11 0.0
