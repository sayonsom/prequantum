---
name: single-qubit-state-reviewer
description: Review a supplied two-entry one-qubit state array, validate it, normalize it when requested, and explain its standard-basis probabilities. Use for array-based exercises before formal quantum notation is introduced.
---

# Single-qubit state reviewer

1. Place the input into the representation, invariant, transformation, and observation map.
2. Confirm that the representation contains exactly two finite numeric amplitudes.
3. Reject the zero vector and calculate the norm.
4. Normalize only when requested, and label normalization as a teaching computation.
5. Calculate both squared-magnitude probabilities and verify that they sum to one within a stated tolerance.
6. If a matrix is supplied, validate its shape, apply it, and recheck the invariant.
7. Keep the explanation in array notation unless the learner requests formal notation.
8. End with one prediction question and a short NumPy verification.
