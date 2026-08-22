from math import gcd

import numpy as np


def modular_multiplication_matrix(base, modulus, width):
    if modulus <= 2 or modulus >= 2**width:
        raise ValueError("modulus must fit strictly inside the register domain")
    if gcd(base, modulus) != 1:
        raise ValueError("base must be invertible modulo the modulus")

    size = 2**width
    matrix = np.zeros((size, size), dtype=complex)
    mapping = {}
    for y in range(size):
        mapped = (base * y) % modulus if y < modulus else y
        mapping[y] = mapped
        matrix[mapped, y] = 1.0
    return matrix, mapping


base = 2
modulus = 15
width = 4
matrix, mapping = modular_multiplication_matrix(base, modulus, width)

assert len(set(mapping.values())) == 2**width
assert all(mapping[y] == (base * y) % modulus for y in range(modulus))
assert all(mapping[y] == y for y in range(modulus, 2**width))
assert np.allclose(matrix.conj().T @ matrix, np.eye(2**width))
assert np.allclose(np.linalg.matrix_power(matrix, 4), np.eye(2**width))

try:
    modular_multiplication_matrix(base=3, modulus=15, width=4)
except ValueError as error:
    rejected_message = str(error)
else:
    raise AssertionError("a non-invertible base should have been rejected")

print(f"mapping_0_to_14={[mapping[y] for y in range(modulus)]}")
print("outside_label_15=fixed")
print("unitary=True")
print("fourth_power_is_identity=True")
print(f"rejected_noninvertible_base={rejected_message}")
