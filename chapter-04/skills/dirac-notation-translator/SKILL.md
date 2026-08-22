---
name: dirac-notation-translator
description: Translate finite-dimensional pure-state Dirac notation into typed NumPy operations while checking basis order, dimensions, normalization, conjugation, operator order, and measurement scope. Use for educational expressions involving kets, bras, inner products, outer products, tensor products, and square operators. Do not use this Skill to certify hardware behavior or to analyze mixed states without a separate density-matrix procedure.
---

# Dirac notation translator

## Required input

- The expression to translate.
- The dimension and ordered basis for each subsystem.
- The tensor-factor and displayed-bit convention.
- Definitions for named states and operators.
- The measurement interpretation being requested, if any.

## Review procedure

1. Tokenize the expression into kets, bras, scalars, operators, tensor products, inner products, and outer products.
2. Assign a dimension and expected NumPy shape to every object.
3. Reject any multiplication whose adjacent dimensions do not agree.
4. Expand named kets into the declared ordered basis only when coordinates are needed.
5. Translate a vector inner product with np.vdot(a, b), which conjugates the first vector.
6. Translate an outer product with np.outer(a, b.conj()).
7. Call |a><a| a projector only when a is normalized; do not call a general |a><b| a projector.
8. Translate tensor factors in the declared order and restate the bit-label mapping before interpreting indices.
9. Evaluate operator composition from the ket outward, which is right to left in the written product.
10. Check normalization of every state and unitarity of every claimed square gate within a stated tolerance.
11. Separate an inner-product amplitude from its squared magnitude and state the rank-one or basis measurement that gives the latter a probability meaning.
12. Treat normalized kets whose squared overlap is one as equivalent up to global phase; do not erase relative phase.

## Output

Return the declared conventions, typed expression tree, dimension ledger, NumPy translation, intermediate arrays, invariant checks, final mathematical object, physical interpretation, and any unresolved ambiguity. Mark missing definitions as "not supplied" and do not invent them.

## Boundaries

- Do not infer an SDK's bit order from this chapter's NumPy convention.
- Do not treat a one-dimensional NumPy array as having row or column orientation without adding an axis.
- Do not use np.dot(a, b) as a general complex inner product when a represents a ket converted to a bra.
- Do not turn an amplitude into a probability without squared magnitude, normalization, and a stated outcome model.
- Do not treat every square matrix as unitary or physically available.
- Do not infer noise, hardware execution, algorithmic speedup, or application value from notation alone.
