---
name: quantum-gate-sequence-reviewer
description: Review finite-dimensional pure-state gate sequences by checking declared basis order, matrix dimensions, unitarity, application order, intermediate states, global-phase equivalence, and measurement scope. Use for educational NumPy gate sequences and decomposition checks. Do not use this Skill to certify hardware executability, noise behavior, or backend calibrations.
---

# Quantum gate sequence reviewer

## Required input

- The initial state and its ordered basis.
- Every gate matrix and the subsystem on which it acts.
- The written gate sequence and the intended chronological order.
- The tensor-factor and displayed-bit convention for multi-qubit work.
- The requested comparison rule: exact equality, equality up to global phase, or approximation within a stated metric and tolerance.
- The measurement basis, if probabilities are requested.

## Review procedure

1. Convert each supplied state and gate to a finite complex array and reject non-finite entries.
2. Check that the state dimension agrees with the declared basis.
3. Check that every gate is nonempty and square and that adjacent dimensions agree.
4. Verify U dagger U equals identity within the supplied tolerance for each claimed deterministic closed-system gate.
5. Restate the chronological gate order and the corresponding right-to-left matrix product.
6. Apply one gate at a time and record every intermediate state.
7. Check normalization after every unitary step.
8. Compare matrices with the requested rule. For global-phase equivalence, require one common unit-magnitude scalar for the complete matrix or state.
9. If probabilities are requested, calculate squared magnitudes only after the final state and measurement basis are identified.
10. For controlled or tensor-product gates, restate the control, target, tensor order, and basis-label-to-index mapping.
11. Separate exact construction, approximate synthesis, and target-specific compilation claims.
12. Report missing conventions as unresolved rather than guessing them.

## Output

Return the declared conventions, dimension ledger, unitarity results, chronological trace, intermediate arrays, equivalence rule and result, final probabilities when requested, and unresolved assumptions.

## Boundaries

- A passing matrix review does not prove that a backend supports the gate or decomposition.
- A unitary model does not represent measurement, reset, noise, or a post-selected branch without an additional operation model.
- Equal entrywise magnitudes do not establish equality up to global phase.
- An entangling-capable gate does not entangle every input state.
- Approximate universality does not establish the classical difficulty or practical value of a particular circuit.
- Do not infer a backend Target, connectivity map, duration, error rate, or calibration from a vendor or processor-family name.
