import numpy as np


left = np.array([0.6, 0.8], dtype=complex)
right = np.array([1, 1j], dtype=complex) / np.sqrt(2)

with_kron = np.kron(left, right)
manual = np.array(
    [
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    ]
)

print(np.round(with_kron, 4))
print("manual match:", np.allclose(with_kron, manual))
print("probability sum:", np.sum(np.abs(with_kron) ** 2))

# [0.4243+0.j     0.    +0.4243j 0.5657+0.j     0.    +0.5657j]
# manual match: True
# probability sum: 1.0
