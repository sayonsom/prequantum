import numpy as np


s = 1 / np.sqrt(2)
bell_states = {
    "Phi+": np.array([s, 0, 0, s], dtype=complex),
    "Phi-": np.array([s, 0, 0, -s], dtype=complex),
    "Psi+": np.array([0, s, s, 0], dtype=complex),
    "Psi-": np.array([0, s, -s, 0], dtype=complex),
}
labels = ("00", "01", "10", "11")

for name, state in bell_states.items():
    visible = [label for label, p in zip(labels, np.abs(state) ** 2) if p > 0]
    print(name, np.real_if_close(np.round(state, 4)), visible)

# Phi+ [0.7071 0.     0.     0.7071] ['00', '11']
# Phi- [ 0.7071  0.      0.     -0.7071] ['00', '11']
# Psi+ [0.     0.7071 0.7071 0.    ] ['01', '10']
# Psi- [ 0.      0.7071 -0.7071  0.    ] ['01', '10']
