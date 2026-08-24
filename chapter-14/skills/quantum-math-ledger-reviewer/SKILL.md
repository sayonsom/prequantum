---
name: quantum-math-ledger-reviewer
description: Audit a bounded quantum-mathematics workflow by reconstructing its objects, representations, transformations, invariants, and evidence boundary. Use for eigenproblems, Hamiltonian evolution, Pauli-term circuit synthesis, density matrices, channels, partial traces, or Bloch-vector calculations; do not use to infer unobserved hardware behavior.
---

# Quantum Math Ledger Reviewer

Review the supplied equations, code, and results as four compatible records. Preserve the user's basis, units, and subsystem conventions unless a change is explicitly requested.

## Required records

1. Reconstruct the object record: states, observables, Hamiltonians, channels, subsystems, dimensions, units, coefficients, and assumptions.
2. Reconstruct the representation record: basis and tensor order, array shapes, statevector or density-matrix form, operator or Kraus form, dtype, and normalization.
3. Reconstruct the transformation record: exact or approximate map, parameters, acted-on subsystem, product order, step count, sampling, seeds, and software versions.
4. Reconstruct the invariant/evidence record: required invariants, tolerances, observed values, comparison reference, evidence level, failures, and strongest supported conclusion.

## Review invariants

- Check vector norms, density-matrix Hermiticity, positive semidefiniteness, and unit trace.
- Check observable and Hamiltonian Hermiticity, unitary evolution, channel complete positivity and trace preservation, and partial-trace dimensions as applicable.
- For degenerate observables, calculate outcome projectors for complete eigenspaces. Do not claim that an outcome selects a unique eigenvector.
- Distinguish global phase from relative phase, a wrong time, a wrong sign, or a wrong generator.
- State hbar and other unit conventions. Do not compare times from incompatible Hamiltonian scales.
- For product formulas, record term order, step count, error metric, exact reference, and the range supporting an empirical convergence claim.
- When a product formula is synthesized as a circuit, distinguish left-to-right temporal gate order from right-to-left matrix multiplication, declare the SDK's Pauli-label order, and verify the factor-of-two rotation-angle convention.
- Distinguish a Python circuit-construction loop, coherent segment repetition, target-aware transpilation, independently prepared shots, and a classical parameter sweep. Do not use the word loop as if these operations were equivalent.
- For a channel dilation, distinguish tracing out a workspace from measuring it and retaining a classical result.
- Distinguish a certain phase flip from complete dephasing. Record the channel parameterization instead of relying only on a channel name.
- Use reduced-state entropy as an entanglement measure only when the joint-state assumptions justify it. A mixed reduced state alone does not prove entanglement for an arbitrary mixed joint state.
- Label evidence as analytic, exact numerical, approximate numerical, declared-noise simulation, or hardware observation. Do not promote one level into another.

## Output

Return:

- the four records, marking unknown fields rather than inventing them;
- a compact invariant table with expected value, observed value, tolerance, status, and minimal repair;
- the strongest conclusion supported by the current evidence;
- the smallest next test that would resolve the most important uncertainty.

If an installed implementation is unavailable, present QuantumGridOS Skills or MCP tools as proposed interface contracts and do not claim that they were executed.
