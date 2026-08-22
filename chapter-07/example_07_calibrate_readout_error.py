import numpy as np


# Columns are prepared states; rows are observed states.
calibration_matrix = np.array([
    [0.96, 0.06],
    [0.04, 0.94],
])

ideal_probabilities = np.array([0.70, 0.30])
observed_probabilities = calibration_matrix @ ideal_probabilities
mitigated_probabilities = np.linalg.solve(
    calibration_matrix, observed_probabilities
)

print("Calibration matrix:\n", calibration_matrix)
print("Observed probabilities:", observed_probabilities)
print("Mitigated probabilities:", mitigated_probabilities)
print("Condition number:", np.linalg.cond(calibration_matrix))

assert np.allclose(calibration_matrix.sum(axis=0), 1.0)
assert np.allclose(mitigated_probabilities, ideal_probabilities)
