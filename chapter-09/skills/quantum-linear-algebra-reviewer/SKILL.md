---
name: quantum-linear-algebra-reviewer
description: Review quantum linear algebra by separating abstract states, coordinates, basis matrices, operators, and measurement evidence. Use when checking basis changes, complex inner products, tensor dimensions, projectors, Hermitian or unitary matrices, spectral decompositions, degeneracy, projective measurements, or PCA analogies.
---

# Quantum Linear Algebra Reviewer

Review the work through four views: object, coordinates, transformation, and evidence. Keep these views separate even when two calculations happen to produce the same numerical array.

## 1. Object view

- Name the ambient complex vector space and its dimension.
- Distinguish the vector space from the normalized statevector set and from physical states modulo global phase.
- State the tensor-factor order for composite systems.
- Treat exponential dimension as a storage fact, not by itself as proof of computational advantage.

## 2. Coordinate view

- Name the current basis and place its vectors as columns of a basis matrix.
- For an orthonormal basis matrix `B`, extract coordinates with `B^dagger |psi>` and reconstruct with `B c`.
- Use conjugate transpose, not ordinary transpose, for complex inner products.
- For nonorthonormal bases, require an invertible basis matrix but do not call it unitary.
- Check norm preservation and reconstruction numerically.

## 3. Transformation view

- Label every operation as active or passive.
- An active operator changes the abstract state while the coordinate basis remains fixed.
- A passive coordinate conversion keeps the abstract state fixed while its coordinate list changes.
- If the same numerical matrix occurs in both calculations, state the special algebraic reason and retain the semantic distinction.
- Classify each matrix independently as Hermitian, unitary, normal, positive semidefinite, or projective.
- Treat unitary gates as reversible closed-system evolution, not as every allowed quantum process.

## 4. Evidence view

- Match each mathematical claim to an invariant, reconstruction test, or executable assertion.
- Distinguish exact statevector calculations from sampled measurement outcomes.
- Do not infer equality of states from one measurement distribution.
- Treat global phase as physically irrelevant and relative phase as observable through an appropriate basis.
- Bound analogies with data science explicitly; a density matrix is not merely a covariance matrix.

## Projectors and measurement

- Construct a rank-one projector as `|v><v|` only when one vector spans the relevant subspace.
- Verify Hermiticity, idempotence, orthogonality, and completeness of projective measurements.
- Use spectral projectors for degenerate eigenvalues; do not replace a degenerate eigenspace with one arbitrary eigenvector.
- Calculate each Born probability as `<psi|Pi|psi>` and normalize the projected branch when its probability is nonzero.
- Distinguish projective measurements from general POVMs, whose positive effects need not be orthogonal projectors.

## Output

Return:

1. the object, coordinate, transformation, and evidence views;
2. blocking mathematical errors;
3. an active-versus-passive audit;
4. operator classifications and tested invariants;
5. a minimal NumPy counterexample or verification; and
6. the strongest supported conclusion with unresolved limitations.
