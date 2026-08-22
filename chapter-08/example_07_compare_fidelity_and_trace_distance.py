"""Compare state fidelity, trace distance, and discrimination probability."""

import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector, state_fidelity


def trace_distance(rho, sigma):
    difference = rho.data - sigma.data
    eigenvalues = np.linalg.eigvalsh(difference)
    return 0.5 * float(np.sum(np.abs(eigenvalues)))


states = {
    "zero": DensityMatrix(Statevector.from_label("0")),
    "plus": DensityMatrix(Statevector.from_label("+")),
    "mixed": DensityMatrix(np.eye(2) / 2),
}

for left_name, right_name in [("zero", "zero"), ("zero", "plus"), ("zero", "mixed")]:
    left, right = states[left_name], states[right_name]
    fidelity = state_fidelity(left, right)
    distance = trace_distance(left, right)
    lower = 1 - np.sqrt(fidelity)
    upper = np.sqrt(1 - fidelity)
    helstrom_success = (1 + distance) / 2
    print(
        f"{left_name:5s} vs {right_name:5s}: F={fidelity:.6f} "
        f"D={distance:.6f} equal-prior success={helstrom_success:.6f}"
    )
    assert lower - 1e-12 <= distance <= upper + 1e-12

# For two pure states, the upper Fuchs-van de Graaf bound is an equality.
pure_fidelity = state_fidelity(states["zero"], states["plus"])
pure_distance = trace_distance(states["zero"], states["plus"])
assert np.isclose(pure_distance, np.sqrt(1 - pure_fidelity))
