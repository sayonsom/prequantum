"""Decompose an arbitrary two-by-two operator in the Pauli basis."""

from __future__ import annotations


Matrix = tuple[tuple[complex, complex], tuple[complex, complex]]

I: Matrix = ((1, 0), (0, 1))
X: Matrix = ((0, 1), (1, 0))
Y: Matrix = ((0, -1j), (1j, 0))
Z: Matrix = ((1, 0), (0, -1))
PAULIS = {"I": I, "X": X, "Y": Y, "Z": Z}


def coefficient(pauli: Matrix, operator: Matrix) -> complex:
    # Pauli matrices are Hermitian, so dagger(pauli) equals pauli.
    product_trace = sum(
        pauli[row][inner] * operator[inner][row]
        for row in range(2)
        for inner in range(2)
    )
    return product_trace / 2


def reconstruct(coefficients: dict[str, complex]) -> Matrix:
    return tuple(
        tuple(
            sum(coefficients[name] * PAULIS[name][row][column] for name in PAULIS)
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


operator: Matrix = ((0.8 + 0.1j, 0.2 - 0.3j), (-0.4j, 0.5))
coefficients = {name: coefficient(pauli, operator) for name, pauli in PAULIS.items()}
rebuilt = reconstruct(coefficients)

for row in range(2):
    for column in range(2):
        assert abs(operator[row][column] - rebuilt[row][column]) < 1e-12

for name, value in coefficients.items():
    print(f"{name}: {value.real:+.3f}{value.imag:+.3f}j")
