"""Apply readout mitigation while reporting numerical diagnostics."""

from __future__ import annotations

import numpy as np


labels = ("00", "01", "10", "11")

# Column j is the distribution of recorded outcomes when state j was prepared.
assignment_matrix = np.array(
    [
        [0.96, 0.02, 0.03, 0.01],
        [0.01, 0.94, 0.01, 0.03],
        [0.02, 0.01, 0.93, 0.02],
        [0.01, 0.03, 0.03, 0.94],
    ]
)
counts = np.array([4770, 247, 286, 4486], dtype=float)
measured = counts / counts.sum()

condition_number = np.linalg.cond(assignment_matrix)
unconstrained, *_ = np.linalg.lstsq(assignment_matrix, measured, rcond=None)
mitigated = np.clip(unconstrained, 0.0, None)
mitigated /= mitigated.sum()

reconstructed = assignment_matrix @ mitigated
residual = np.linalg.norm(reconstructed - measured, ord=1)

def rounded_record(values: np.ndarray) -> dict[str, float]:
    return {label: round(float(value), 4) for label, value in zip(labels, values)}


print("Measured:   ", rounded_record(measured))
print("Unconstrained estimate:", rounded_record(unconstrained))
print("Mitigated:  ", rounded_record(mitigated))
print(f"condition number={condition_number:.3f}")
print(f"L1 reconstruction residual={residual:.6f}")

assert np.allclose(assignment_matrix.sum(axis=0), 1.0)
assert np.isclose(mitigated.sum(), 1.0)
assert np.all(mitigated >= 0.0)
