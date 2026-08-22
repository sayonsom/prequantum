---
name: hamiltonian-simulation-reviewer
description: Audit a Hamiltonian-simulation workflow from system definition through operator terms, evolution, observation, and evidence. Use when commutators, product formulas, circuit decompositions, measurement claims, molecular mappings, or quantum-simulation resource claims need verification.
---

# Hamiltonian Simulation Reviewer

Review the supplied model, code, circuits, results, and provenance as five compatible records: system, Hamiltonian, evolution, observation, and evidence. Preserve the user's intended scientific question. Do not silently repair the model into a different one.

## Reconstruct the records

1. Record the basis labels and order, qubit convention, initial state or preparation circuit, units, boundary conditions, and modeling assumptions.
2. Record every Hamiltonian term, coefficient, sign, operator order, mapping, source, and constant contribution.
3. Record total time, hbar convention, exact or approximate method, term grouping, multiplication order, formula order, repetitions, compiler settings, and target.
4. Record every requested observable, basis rotation, grouping, shots, seed, estimator, uncertainty calculation, and post-processing step.
5. Record exact or classical references, approximation metric, statistical error, noise model, backend provenance, logical and transpiled resources, failures, and the strongest supported claim.

## Check invariants

- Validate dimensions, finite values, initial-state normalization, basis order, and operator Hermiticity.
- Reconstruct the Hamiltonian from the recorded terms. Reject a missing term, duplicated coefficient, silent unit conversion, or unrecorded constant.
- Compute pairwise commutators before accepting a product-formula rationale. Commuting terms may be grouped or exponentiated exactly; nonzero commutators must appear in the approximation discussion.
- Compare each compiled Pauli-evolution block with an exact small matrix when tractable. Include gate rotation conventions and qubit order.
- Compare the full approximate evolution with an exact reference across several step counts and at least one declared metric. Separate product-formula bias from floating-point error.
- Treat a randomized method as a channel or ensemble. Record seeds and trial counts; do not describe one trajectory as the method average.
- Reconstruct observable estimates from outcomes. Keep approximation error, shot uncertainty, mitigation, and hardware noise as separate fields.
- For molecular operators, retain geometry, basis, active space, fermion-to-qubit mapping, symmetry reduction, and nuclear-repulsion handling when those data are available. Mark missing metadata unknown.
- Classify evidence as algebraic, exact reference, ideal circuit, noisy simulation, hardware experiment, or comparative resource study. Do not infer advantage from Hilbert-space dimension, qubit count, a simulator result, or a proof-of-concept circuit.
- For HHL or another linear-system bridge, record input and readout assumptions, conditioning, state preparation, success probability, and whether the numerical solution was actually produced by the quantum path.

## Report

Return the five reconstructed records, an invariant table with observed and expected values, every mismatch and its smallest repair, and a conclusion bounded by the executed evidence. Mark unknown fields explicitly. If a QuantumGridOS Skill, MCP server, solver, or plugin is unavailable or incomplete, describe it as proposed or provisional and do not claim it was executed or deployed.
