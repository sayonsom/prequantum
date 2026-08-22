"""Build tensor-product dimensions without treating dimension as an advantage proof."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)

state = np.array([1.0], dtype=complex)
for qubit_count in range(1, 7):
    state = np.kron(state, zero)
    expected_dimension = 2**qubit_count
    print(
        f"qubits={qubit_count} dimension={state.size} "
        f"nonzero_amplitudes={np.count_nonzero(state)}"
    )
    assert state.size == expected_dimension
    assert np.count_nonzero(state) == 1

# The ambient dimension grows exponentially, but this particular product state
# still has a compact preparation rule. Dimension alone proves no speedup.
