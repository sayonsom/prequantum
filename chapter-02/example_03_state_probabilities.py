import numpy as np

state = np.array([0.6, 0.8], dtype=complex)
probabilities = np.abs(state) ** 2

print(probabilities)
print(np.sum(probabilities))
print(np.allclose(np.sum(probabilities), 1.0))
# [0.36 0.64]
# 1.0
# True
