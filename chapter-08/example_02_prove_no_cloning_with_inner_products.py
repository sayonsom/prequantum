"""Use preservation of inner products to expose the no-cloning contradiction."""

import numpy as np


zero = np.array([1.0, 0.0], dtype=complex)
one = np.array([0.0, 1.0], dtype=complex)
plus = (zero + one) / np.sqrt(2)


def overlap(left, right):
    return np.vdot(left, right)


def compare_required_overlaps(name, psi, phi):
    input_overlap = overlap(np.kron(psi, zero), np.kron(phi, zero))
    clone_overlap = overlap(np.kron(psi, psi), np.kron(phi, phi))
    print(
        f"{name:17s} input={input_overlap:.6f} "
        f"required-output={clone_overlap:.6f}"
    )
    return input_overlap, clone_overlap


orthogonal = compare_required_overlaps("|0> and |1>", zero, one)
nonorthogonal = compare_required_overlaps("|0> and |+>", zero, plus)
identical = compare_required_overlaps("|+> and |+>", plus, plus)

# A unitary must preserve the input overlap. A universal cloner would square it.
assert np.isclose(orthogonal[0], orthogonal[1])
assert not np.isclose(nonorthogonal[0], nonorthogonal[1])
assert np.isclose(identical[0], identical[1])
