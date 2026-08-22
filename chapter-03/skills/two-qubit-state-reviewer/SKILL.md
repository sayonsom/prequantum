---
name: two-qubit-state-reviewer
description: Review a supplied four-entry two-qubit pure-state array, its ordering convention, transformations, and measurement claims. Use for NumPy teaching examples before density matrices are introduced. Do not use this pure-state procedure to certify noisy hardware entanglement or mixed-state entanglement.
---

# Two-qubit state reviewer

## Required input

- The four-entry state array.
- The declared mapping from array indices to bit labels.
- The transformations applied in order.
- The measurement basis and the claim being evaluated.

## Review procedure

1. Confirm that the array has exactly four finite complex entries and nonzero norm.
2. Normalize a copy and report whether the supplied array was already normalized.
3. Restate the bit-ordering and tensor-factor convention before interpreting any index.
4. Verify that every gate has shape four by four and is unitary within tolerance.
5. Recompute every intermediate state and its standard-basis probabilities.
6. Reshape the final normalized pure state into a two-by-two coefficient matrix.
7. Use the determinant-zero test only to classify separability of this two-qubit pure state.
8. Separate amplitude structure, measurement distribution, sampled counts, and hardware evidence.
9. Reject any claim that perfect correlation in one basis alone proves nonclassicality.
10. State which additional model or evidence is needed for a mixed state, noisy execution, or Bell-test claim.

## Output

Return the convention, validation results, intermediate-state table, separability result with scope, measurement interpretation, unsupported-claim list, and next evidence required. Mark unavailable information as "not supplied" and do not invent it.

## Boundaries

- Do not infer an SDK's bit order from this chapter's NumPy convention.
- Do not treat the determinant shortcut as a mixed-state entanglement test.
- Do not treat entanglement as proof of speedup or application advantage.
- Do not describe local random outcomes as controllable messages.
