---
name: shor-order-finding-reviewer
description: Review Shor order-finding demonstrations and claims through explicit arithmetic, reversible-unitary, phase-recovery, and evidence-resource records. Use when checking a factoring example, modular-multiplication oracle, QFT or QPE convention, continued-fraction recovery, or resource claim. Do not use to certify undeclared hardware feasibility or cryptographic break capability.
---

# Shor Order-Finding Reviewer

Review the supplied demonstration or claim through four linked records. Do not accept a factor, period, runtime, or cryptographic conclusion until the records use compatible assumptions.

## Arithmetic reduction record

- Record the composite integer, its input bit length, and any classical prechecks.
- Record the base-selection rule and compute the initial greatest common divisor.
- Define the multiplicative order as the least positive r satisfying a^r congruent to one modulo N.
- Verify an alleged order directly; do not accept a hard-coded or unvalidated value.
- For factoring, require an even order and reject the case a^(r/2) congruent to minus one modulo N.
- Recompute both greatest common divisors and distinguish factors from trivial outputs.

## Reversible-unitary record

- Define modular multiplication on every computational-basis label, including labels outside the arithmetic domain.
- Require the base to be invertible modulo the modulus.
- Record target, counting, workspace, and classical-register order.
- Record each controlled power and how it is implemented rather than treating a dense unitary as scalable arithmetic.
- Verify reversibility, workspace initialization, uncomputation, and bit-order conventions.

## Phase-recovery record

- State the unitary-eigenstate promise and write the eigenvalue as a phase in the interval from zero inclusive to one exclusive.
- Record counting precision, controlled-power order, QFT sign, final-swap convention, measurement mapping, and displayed-bit order.
- Treat a measured value as a sample from a distribution, not as a guaranteed exact phase.
- Run continued fractions under a declared denominator bound.
- Allow a recovered denominator to be a proper divisor of the complete order.
- Combine repeated evidence conservatively, validate candidate multiples, and reduce to the least order when possible.

## Evidence and resource record

- Label evidence as derivation, exact matrix, ideal statevector, ideal sampled simulation, declared noise simulation, compiled circuit, fault-tolerant estimate, or hardware observation.
- Count controlled modular powers separately from their arithmetic gate implementations.
- Keep high-level calls, logical gates, logical qubits, logical cycles, error-correction assumptions, physical resources, repetitions, and wall-clock estimates in separate fields.
- Require an immutable circuit or arithmetic-construction identifier for comparisons.
- Do not infer cryptographic-scale feasibility from a toy factorization or a dense-unitary simulator.
- Do not treat a dated resource estimate as a hardware observation.

## Required checks

- Test the modular mapping on every basis label for small domains and verify unitarity.
- Compare the QFT circuit with the declared matrix, including the bit-reversal permutation.
- Compare phase-estimation probabilities with the geometric-series formula for a non-binary phase.
- Verify every continued-fraction candidate with modular exponentiation.
- Exercise zero outcomes, reduced denominators, odd orders, and trivial greatest-common-divisor cases.
- State the strongest conclusion supported by the weakest evidence level in the complete pipeline.

## Output

Return:

1. the four records;
2. blocking arithmetic, unitary, phase, or evidence errors;
3. a basis-order and register-order ledger;
4. a phase, fraction, denominator, and candidate-validation table;
5. a high-level, compiled, logical, and physical resource ledger;
6. minimal executable checks; and
7. the strongest supported conclusion with excluded costs and missing evidence.
