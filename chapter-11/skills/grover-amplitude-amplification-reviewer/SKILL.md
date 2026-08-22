---
name: grover-amplitude-amplification-reviewer
description: Review Grover search and amplitude-amplification implementations through explicit search, oracle, rotation, and evidence records. Use when checking marked predicates, phase oracles, diffusers, iteration schedules, multiple or unknown solution counts, Qiskit bit order, query and shot counts, synthetic noise, or claimed quadratic advantage.
---

# Grover Amplitude Amplification Reviewer

Review the supplied algorithm through four linked records. Do not accept a speedup or success claim until the records use compatible assumptions.

## Search record

- Define the finite domain and Boolean marked predicate.
- State whether zero, one, or multiple labels may be marked and whether the marked count is known.
- State the required output, input distribution, success probability, and error criterion.
- Distinguish an abstract query domain from a stored list or database requiring a data-access implementation.

## Oracle record

- Write the value-oracle and phase-oracle mappings and their relationship through phase kickback.
- Build the phase reflection from the projector onto the complete marked subspace.
- Name register, tensor, qubit, and displayed-bit order.
- Verify reversibility, workspace initialization, and uncomputation.
- State whether the predicate is available only through queries or its implementation can be inspected.

## Rotation record

- Define the prepared state and its normalized good and bad components.
- Calculate the initial good probability and theta.
- Verify the phase-marking reflection and the reflection about the prepared state.
- Derive the exact finite-iteration success probability and test adjacent integer counts around the first peak.
- Treat repeated Grover steps as a rotation, not a monotonic convergence method.
- For an unknown marked count, require a valid randomized search schedule or counting or estimation procedure; reject naive deterministic doubling.
- For general amplitude amplification, count state preparation and inverse preparation as well as marking queries.

## Evidence and cost record

- Count marking-oracle applications per circuit execution.
- Count verification queries, retries, circuit executions, and shots separately.
- Label evidence as exact derivation, statevector calculation, ideal sampled simulation, declared noise simulation, or hardware observation.
- Record compiled gate counts, two-qubit depth, routing, and the complete noise-model declaration when they support the claim.
- Do not infer wall-clock, database, cryptanalytic, or economic advantage from query complexity alone.
- Do not generalize a synthetic error model to current hardware.

## Required checks

- Test the oracle on every basis input for small domains and verify unitarity.
- Verify that the diffuser has eigenvalue plus one on the prepared direction and minus one on orthogonal directions.
- Check the theoretical and numerical good-subspace probabilities after every reported iteration.
- Use asymmetric bit strings and the all-zero label to expose open-control and reversal errors.
- Verify that the classical comparison uses the same promise, access restriction, and success criterion.

## Output

Return:

1. the four records;
2. blocking correctness or comparison errors;
3. an oracle, workspace, and bit-order audit;
4. an exact iteration and success-probability table;
5. a query, verification, retry, shot, and compiled-cost ledger;
6. a minimal executable verification; and
7. the strongest supported advantage claim with excluded costs and evidence gaps.
