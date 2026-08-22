---
name: power-system-quantum-workflow-reviewer
description: Audit power-system optimization and quantum-optimization workflows from physical model through formulation, solver execution, feasibility checks, and evidence. Use when unit commitment, dispatch, power flow, QUBO, QAOA, grid-integration, or claimed quantum advantage needs verification.
---

# Power-System Quantum Workflow Reviewer

Review the supplied model, code, results, and provenance as five compatible
records: physical grid, planning problem, formulation, solver run, and
evidence. Preserve the user's stated operational question. Do not silently
replace it with a capacity-selection toy or a different power-flow model.

## Reconstruct the records

1. Record buses, branches, generators, loads, units, base values, sign
   conventions, reference bus, time resolution, forecasts, scenarios, and
   every modeling approximation.
2. Record decision variables and domains, objective terms, constraint
   equations, initial conditions, time coupling, reserve or contingency scope,
   and the distinction between commitment and dispatch.
3. Record every transformation into MILP, LP, QP, QUBO, Ising, or circuit
   form, including scaling, discretization, auxiliary variables, penalty
   coefficients, qubit order, and the information discarded by the mapping.
4. Record solver name and version, settings, seed, termination status, bounds,
   runtime boundary, backend, shots, calibration context, and returned raw
   candidates.
5. Record independent feasibility checks, exact or classical baselines,
   optimality gap when available, network and contingency validation,
   software and data hashes, authorization boundary, and strongest supported
   claim.

## Check invariants

- Validate dimensions, finite values, time indexes, unit conversions, base
  values, and the declared injection sign convention.
- Separate binary commitment status from continuous power dispatch. Check
  minimum and maximum output only when a unit is on, and check power balance
  using dispatched power rather than nameplate capacity.
- Check startup, shutdown, ramp, minimum-up, minimum-down, reserve, and initial
  conditions whenever the planning problem claims to include them. Mark each
  omitted family explicitly.
- For DC power flow, require a reference angle, balanced net injections, a
  connected reduced susceptance matrix, consistent per-unit conversion, nodal
  balance, and branch-flow reconstruction. Treat the DC model as an
  approximation; do not infer AC feasibility from a small angle alone.
- For transmission-constrained dispatch, recompute every monitored flow and
  limit. A capacity-feasible commitment is not network feasible until this
  subproblem passes. A base-case check is not contingency security.
- For a finite QUBO, decode every auxiliary bit and enumerate all states when
  tractable. Compare the best feasible objective with every infeasible energy,
  report strict penalty thresholds and ties, and distinguish encoding
  feasibility from sampler success.
- Treat QAOA, annealing, and other binary optimizers as candidate generators
  unless the executed workflow proves more. Do not infer speedup or advantage
  from problem hardness, Hilbert-space size, qubit count, or a simulator run.
- Inspect library source at an immutable version before describing an API.
  Mark placeholders, classical fallbacks, missing imports, unimplemented
  authorization, and unexecuted paths. Do not describe a formatter as a live
  grid integration.
- Keep read-only analysis separate from operational control. A schedule must
  not be described as approved, dispatched, or SCADA-integrated without the
  relevant external authorization and system evidence.

## Report

Return the five reconstructed records, an invariant table with observed and
expected values, every mismatch and its smallest repair, and a conclusion
bounded by the executed evidence. Mark unknown fields explicitly. Classify
evidence as algebraic derivation, exact finite enumeration, classical solver,
ideal quantum simulation, noisy quantum simulation, hardware experiment, or
operational validation. If a QuantumGridOS Skill, MCP server, solver, plugin,
or operational interface is unavailable or incomplete, describe it as
proposed or provisional and do not claim that it was executed or deployed.
