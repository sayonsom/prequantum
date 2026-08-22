---
name: variational-run-reviewer
description: Audit a bounded VQE, QAOA, or related variational-quantum run by reconstructing its objective, state family, evaluation plan, and evidence ledger. Use for technical review or debugging, not for claiming untested hardware performance or quantum advantage.
---

# Variational Run Reviewer

Review the supplied workflow as four compatible records. Preserve the user's problem definition and code unless a change is explicitly requested.

## Required records

1. Reconstruct the objective/operator record: problem instance, variable-to-qubit mapping, Pauli operator, coefficient signs, constant offset, optimization direction, and classical reference.
2. Reconstruct the state-family record: initial state, ansatz, parameter domains, depth, connectivity, symmetry constraints, and relevant reachability limits.
3. Reconstruct the evaluation/optimization record: analytic or sampled estimator, grouping rule, shots, uncertainty, optimizer, initialization, seeds, restarts, and stopping rule.
4. Reconstruct the evidence/resource record: evidence level, observations, comparison, quantum and classical resources, excluded costs, limitations, and strongest supported conclusion.

## Review invariants

- Recompute signs, offsets, and bit mappings from the problem statement rather than trusting labels.
- Apply the variational lower bound only to the exact expectation of a normalized prepared state. A finite-shot or noisy estimate can fluctuate below the exact ground energy.
- Distinguish commuting Pauli operators from qubit-wise commuting terms that share a simple tensor-product measurement basis. Preserve covariance when terms reuse samples.
- Distinguish the optimum over a declared ansatz from the value returned by a particular optimizer run.
- Compare small instances with an exact or credible classical reference when practical.
- Label evidence as analytic, ideal statevector, finite-shot simulation, noise-model simulation, or hardware observation. Do not promote one level into another.
- Reject scalable-advantage conclusions that lack a credible classical comparison and end-to-end resource accounting.

## Output

Return:

- the four completed records, marking unknown fields instead of inventing values;
- a compact failure table with invariant, evidence, status, and minimal repair;
- the strongest conclusion supported by the current evidence;
- the smallest next experiment that would resolve the most important uncertainty.

If an installed implementation is not available, present proposed QuantumGridOS Skills or MCP tools as interface contracts and do not claim that they were executed.
