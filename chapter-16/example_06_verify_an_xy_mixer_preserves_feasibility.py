"""Example 16.6: verify that an XY ring mixer preserves Hamming weight."""

import numpy as np
from scipy.linalg import expm


n_qubits = 4
dimension = 2**n_qubits
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)


def one_qubit(operator, location):
    factors = [operator if index == location else I for index in range(n_qubits)]
    result = factors[0]
    for factor in factors[1:]:
        result = np.kron(result, factor)
    return result


def two_qubit(first, i, second, j):
    factors = []
    for index in range(n_qubits):
        if index == i:
            factors.append(first)
        elif index == j:
            factors.append(second)
        else:
            factors.append(I)
    result = factors[0]
    for factor in factors[1:]:
        result = np.kron(result, factor)
    return result


xy_mixer = np.zeros((dimension, dimension), dtype=complex)
for i in range(n_qubits):
    j = (i + 1) % n_qubits
    xy_mixer += 0.5 * (
        two_qubit(X, i, X, j) + two_qubit(Y, i, Y, j)
    )

number_operator = sum(
    (np.eye(dimension, dtype=complex) - one_qubit(Z, i)) / 2.0
    for i in range(n_qubits)
)
commutator_norm = np.linalg.norm(xy_mixer @ number_operator - number_operator @ xy_mixer)

initial = np.zeros(dimension, dtype=complex)
initial[int("1100", 2)] = 1.0
final = expm(-1j * 0.7 * xy_mixer) @ initial
probabilities = np.abs(final) ** 2
leakage = sum(
    probabilities[index]
    for index in range(dimension)
    if format(index, "04b").count("1") != 2
)

print(f"commutator_norm={commutator_norm:.1e}")
print(f"probability_outside_weight_2={leakage:.1e}")
for index in np.argsort(-probabilities, kind="stable"):
    if probabilities[index] > 0.10:
        print(f"bits={format(index, '04b')}, probability={probabilities[index]:.6f}")

