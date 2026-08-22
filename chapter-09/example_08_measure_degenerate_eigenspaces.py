"""Use spectral projectors to measure an observable with degeneracy."""

import numpy as np


# Eigenvalue +1 spans |00> and |01>; eigenvalue -1 spans |10> and |11>.
observable = np.diag([1.0, 1.0, -1.0, -1.0]).astype(complex)
psi = np.array([1.0, 1.0j, 1.0, -1.0j], dtype=complex) / 2

eigenvalues, eigenvectors = np.linalg.eigh(observable)
projectors = {}
for value in np.unique(np.round(eigenvalues, 12)):
    columns = eigenvectors[:, np.isclose(eigenvalues, value)]
    projectors[float(value)] = columns @ columns.conj().T

probabilities = {}
poststates = {}
for value, projector in projectors.items():
    branch = projector @ psi
    probability = float(np.vdot(branch, branch).real)
    probabilities[value] = probability
    poststates[value] = branch / np.sqrt(probability)
    print(f"eigenvalue={value:+.0f} probability={probability:.3f}")

assert np.allclose(sum(projectors.values()), np.eye(4))
assert np.isclose(sum(probabilities.values()), 1.0)
assert np.isclose(probabilities[1.0], 0.5)
assert np.isclose(probabilities[-1.0], 0.5)
assert np.allclose(observable @ poststates[1.0], poststates[1.0])
assert np.allclose(observable @ poststates[-1.0], -poststates[-1.0])

# A degenerate outcome selects an eigenspace. It need not select one eigenvector.
assert np.count_nonzero(np.abs(poststates[1.0]) > 1e-12) == 2
