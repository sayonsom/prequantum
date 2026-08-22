"""Build and verify a reversible value oracle for a Boolean AND function."""

import numpy as np


def function(x0, x1):
    return x0 & x1


# Basis order is |x0 x1 y>; the output is y XOR f(x0, x1).
oracle = np.zeros((8, 8), dtype=complex)
for x0 in (0, 1):
    for x1 in (0, 1):
        for y in (0, 1):
            source = 4 * x0 + 2 * x1 + y
            target = 4 * x0 + 2 * x1 + (y ^ function(x0, x1))
            oracle[target, source] = 1

for x0 in (0, 1):
    for x1 in (0, 1):
        source = 4 * x0 + 2 * x1
        output = oracle @ np.eye(8, dtype=complex)[:, source]
        observed_index = int(np.argmax(np.abs(output)))
        observed_y = observed_index & 1
        print(f"f({x0}{x1})={observed_y}")
        assert observed_y == function(x0, x1)

assert np.allclose(oracle.conj().T @ oracle, np.eye(8))
assert np.allclose(oracle @ oracle, np.eye(8))
