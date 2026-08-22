---
name: quantum-query-algorithm-reviewer
description: Review oracle-based quantum algorithms through explicit promise, oracle, query, and evidence contracts. Use when checking Deutsch-Jozsa, Bernstein-Vazirani, phase kickback, query-complexity claims, Qiskit bit order, shot counts, ideal or noisy results, or a claimed query advantage.
---

# Quantum Query Algorithm Reviewer

Review the supplied algorithm through four independent contracts. Do not accept a speedup conclusion until all four contracts use compatible assumptions.

## Promise contract

- Define the allowed input-function family and the inputs on which behavior is not specified.
- State the required output and success criterion.
- Distinguish exact, deterministic, randomized, and bounded-error guarantees.
- For Deutsch-Jozsa, require the constant-or-balanced promise.
- For Bernstein-Vazirani, require a function of the form `f(x) = s dot x mod 2` and define the semantic order of `s`.

## Oracle contract

- Write the oracle mapping and name the tensor-factor order.
- Verify unitarity or a reversible construction, including any workspace that must be returned to its initial state.
- Distinguish a value oracle from a phase oracle and derive any phase-kickback conversion.
- State whether the function is available only through queries or whether its implementation can be inspected.
- Record Qiskit qubit labels separately from displayed bit-string order.

## Query contract

- Count oracle applications in one circuit execution.
- State the classical comparison model and use the same promise and error criterion.
- Keep exact deterministic Deutsch-Jozsa complexity separate from randomized bounded-error complexity.
- Treat oracle construction, non-query gates, routing, state preparation, measurement, shots, and runtime as costs outside a query-only count.
- Do not infer end-to-end speedup from a smaller query count.

## Evidence contract

- Distinguish one-query circuit structure from the number of circuit executions requested as shots.
- Label evidence as exact algebra, statevector calculation, ideal sampled simulation, declared noise simulation, or hardware observation.
- Require a complete noise-model declaration before interpreting a noisy simulation.
- Do not generalize a synthetic noise result to current hardware.
- Match the conclusion to the observed distribution, finite-shot uncertainty, and bit-order parser.

## Algorithm checks

- For phase kickback, verify the output eigenstate and the relative phase placed on every relevant input component.
- For Deutsch-Jozsa, calculate the all-zero amplitude and reject conclusions for inputs outside the promise.
- For Bernstein-Vazirani, derive the final label from the binary inner product and verify semantic versus displayed order.
- When discussing interference, identify the Walsh-Hadamard amplitude being calculated rather than claiming that all function values are readable.

## Output

Return:

1. the four contracts;
2. blocking correctness or comparison errors;
3. an oracle, tensor-order, and bit-order audit;
4. a query-versus-shots ledger;
5. a minimal executable verification; and
6. the strongest supported advantage claim with excluded costs and evidence gaps.
