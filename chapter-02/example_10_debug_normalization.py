import numpy as np


class BuggyQubit:
    def __init__(self, values):
        self.state = np.asarray(values, dtype=complex)
        squared_norm = np.sum(np.abs(self.state) ** 2)
        self.state = self.state / squared_norm


model = BuggyQubit([3, 4])
print(model.state)
print(np.sum(np.abs(model.state) ** 2))
# [0.12+0.j 0.16+0.j]
# 0.04
