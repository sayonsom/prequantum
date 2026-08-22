import numpy as np


H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=complex,
)

start = np.array([1, 0, 0, 0], dtype=complex)
after_h = np.kron(H, I) @ start
after_cnot = CNOT @ after_h

for name, state in (
    ("start", start),
    ("after_h", after_h),
    ("after_cnot", after_cnot),
):
    print(
        name,
        np.real_if_close(np.round(state, 4)),
        np.round(np.abs(state) ** 2, 4),
    )

# start [1. 0. 0. 0.] [1. 0. 0. 0.]
# after_h [0.7071 0.     0.7071 0.    ] [0.5 0.  0.5 0. ]
# after_cnot [0.7071 0.     0.     0.7071] [0.5 0.  0.  0.5]
