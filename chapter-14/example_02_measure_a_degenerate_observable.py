import numpy as np


I = np.eye(2, dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
observable = np.kron(Z, I)

# This normalized state has support in both eigenspaces of Z tensor I.
state = np.array([1, 1j, 2, -1], dtype=complex)
state = state / np.linalg.norm(state)

eigenvalues, eigenvectors = np.linalg.eigh(observable)
distinct_values = sorted(set(np.round(eigenvalues, 12)))
projectors = {}
probabilities = {}
post_measurement_states = {}

for value in distinct_values:
    columns = eigenvectors[:, np.isclose(eigenvalues, value)]
    projector = columns @ columns.conj().T
    probability = float(np.real(state.conj() @ projector @ state))
    projected = projector @ state
    post_state = projected / np.sqrt(probability)
    projectors[value] = projector
    probabilities[value] = probability
    post_measurement_states[value] = post_state

assert np.allclose(sum(projectors.values()), np.eye(4))
assert np.isclose(sum(probabilities.values()), 1.0)
for value, projector in projectors.items():
    assert np.allclose(projector, projector.conj().T)
    assert np.allclose(projector @ projector, projector)
    post_state = post_measurement_states[value]
    assert np.allclose(observable @ post_state, value * post_state)

print(f"eigenvalues_with_multiplicity={eigenvalues}")
for value in distinct_values:
    rank = int(round(np.trace(projectors[value]).real))
    print(f"outcome={value:+.0f}, eigenspace_rank={rank}, probability={probabilities[value]:.6f}")
    print(f"post_measurement_state={np.round(post_measurement_states[value], 6)}")
print("interpretation=a degenerate outcome selects an eigenspace, not a unique basis vector")
