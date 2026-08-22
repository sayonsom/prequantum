"""Show why CNOT copies two basis labels but does not clone an arbitrary state."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
one = np.array([0.0, 1.0], dtype=complex)
plus = (zero + one) / np.sqrt(2)

# Basis order: |00>, |01>, |10>, |11>. The first qubit controls.
cnot = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)

tests = {"|0>": zero, "|1>": one, "|+>": plus}

for label, state in tests.items():
    actual = cnot @ np.kron(state, zero)
    requested_copy = np.kron(state, state)
    print(f"{label:3s}  actual={np.round(actual, 3)}")
    print(f"     copy  ={np.round(requested_copy, 3)}")
    print(f"     match ={np.allclose(actual, requested_copy)}")

assert np.allclose(cnot @ np.kron(zero, zero), np.kron(zero, zero))
assert np.allclose(cnot @ np.kron(one, zero), np.kron(one, one))
assert not np.allclose(cnot @ np.kron(plus, zero), np.kron(plus, plus))
