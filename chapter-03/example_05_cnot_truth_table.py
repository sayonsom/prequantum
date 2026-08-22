import numpy as np


CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)
labels = ("00", "01", "10", "11")

for input_index, input_label in enumerate(labels):
    state = np.eye(4, dtype=complex)[:, input_index]
    output = CNOT @ state
    output_label = labels[int(np.argmax(np.abs(output)))]
    print(input_label, "->", output_label)

print("unitary:", np.allclose(CNOT.conj().T @ CNOT, np.eye(4)))

# 00 -> 00
# 01 -> 01
# 10 -> 11
# 11 -> 10
# unitary: True
