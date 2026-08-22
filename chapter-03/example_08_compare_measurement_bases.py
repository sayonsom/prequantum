import numpy as np


def same_result_probability(probabilities: np.ndarray) -> float:
    return float(probabilities[0] + probabilities[3])


H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
HH = np.kron(H, H)
basis = np.eye(4, dtype=complex)
bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)

bell_standard = np.abs(bell) ** 2
classical_standard = np.array([0.5, 0.0, 0.0, 0.5])

bell_hadamard = np.abs(HH @ bell) ** 2
classical_hadamard = (
    0.5 * np.abs(HH @ basis[:, 0]) ** 2
    + 0.5 * np.abs(HH @ basis[:, 3]) ** 2
)

for name, probabilities in (
    ("Bell, standard", bell_standard),
    ("classical mixture, standard", classical_standard),
    ("Bell, Hadamard", bell_hadamard),
    ("classical mixture, Hadamard", classical_hadamard),
):
    print(name, np.round(probabilities, 3), same_result_probability(probabilities))

# Bell, standard [0.5 0.  0.  0.5] 0.9999999999999998
# classical mixture, standard [0.5 0.  0.  0.5] 1.0
# Bell, Hadamard [0.5 0.  0.  0.5] 0.9999999999999996
# classical mixture, Hadamard [0.25 0.25 0.25 0.25] 0.4999999999999998
