---
name: qubo-formulation-reviewer
description: Audit a binary optimization model from its original decision problem through QUBO or Ising encoding and solver evidence. Use when coefficients, penalties, slack variables, bit order, decoded feasibility, baselines, or quantum-optimization claims need verification.
---

# QUBO Formulation Reviewer

Review the supplied problem statement, formulation, code, coefficients, and results as five compatible records: decision, objective, feasibility, solver, and evidence. Preserve the user's intended optimization problem. Do not silently repair it into a different problem.

## Reconstruct the records

1. Record every decision variable, domain, unit, index order, and decoding rule.
2. Record the objective sense, constant, linear terms, pair terms, and any scaling or normalization.
3. Record each original constraint separately from its penalty or structural encoding. For inequalities, identify every slack variable, range, and bit weight.
4. Record the QUBO convention, binary-to-spin substitution, Hamiltonian term order, initial state, mixer, optimizer, seed, shots, backend, compilation settings, and stopping rule when applicable.
5. Record exact or classical baselines, feasibility checks after decoding, objective values in original units, timing boundaries, uncertainty, failures, and the strongest supported claim.

## Check invariants

- Expand each penalty algebraically using the declared binary identity x_i^2 = x_i. Compare the direct constrained objective with the compiled polynomial on every assignment when enumeration is tractable; otherwise use boundary cases and randomized property tests.
- Require one explicit QUBO storage convention. For an upper-triangular matrix, store each pair coefficient once. For a symmetric matrix evaluated by x^T Q x, split each pair coefficient across the two mirrored entries. Reject an unexplained mixture.
- Keep the constant offset even when it does not affect the minimizing assignment, because it is required for energy equality and cross-representation comparisons.
- Distinguish an equality penalty from an inequality. Do not replace a less-than-or-equal constraint with equality unless bounded slack or another exact encoding is present.
- Establish a penalty bound or sweep. Check that the best infeasible energy is strictly above the best feasible energy, then report coefficient range and objective resolution after any rescaling.
- Verify x_i = (1 - z_i)/2 or the user's declared alternative on all tractable assignments before accepting an Ising or Pauli Hamiltonian.
- For a constraint-preserving mixer, check that the initial state is feasible and that the mixer preserves the declared feasible subspace. A commuting conserved quantity is evidence only for the constraint it represents.
- Treat QAOA, quantum annealing, simulated annealing, and exact enumeration as different execution records. Decode and evaluate every returned sample with the original objective and constraints.
- Do not infer computational advantage from search-space size, Hilbert-space dimension, a successful toy instance, approximation quality alone, or a simulator result. Require a relevant classical baseline and a declared end-to-end resource comparison.

## Report

Return the reconstructed five records, an invariant table with observed and expected values, every mismatch and its smallest repair, and a conclusion bounded by the available evidence. Mark unknown fields explicitly. If a QuantumGridOS Skill, MCP server, solver, or plugin is unavailable, describe it as proposed and do not claim it was executed or deployed.

