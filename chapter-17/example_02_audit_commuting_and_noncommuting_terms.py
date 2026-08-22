"""Compute commutators before choosing a product formula."""

import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def commutator_norm(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a @ b - b @ a, ord=2))


families = {
    "two-spin Heisenberg terms": {
        "XX": np.kron(X, X),
        "YY": np.kron(Y, Y),
        "ZZ": np.kron(Z, Z),
    },
    "transverse-field Ising terms": {
        "ZZ": np.kron(Z, Z),
        "XI": np.kron(X, I),
        "IX": np.kron(I, X),
    },
}

for family_name, terms in families.items():
    print(family_name)
    labels = list(terms)
    for left_index, left in enumerate(labels):
        for right in labels[left_index + 1 :]:
            value = commutator_norm(terms[left], terms[right])
            relation = "commute" if np.isclose(value, 0.0) else "do not commute"
            print(f"  [{left}, {right}] norm = {value:.1f} -> {relation}")

