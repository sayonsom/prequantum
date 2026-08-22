---
name: qiskit-circuit-contract-reviewer
description: Review supplied Qiskit circuit code or diagrams for operation order, bit conventions, measurement mappings, execution-interface fit, dependency depth, and reproducibility metadata. Use for local educational circuit reviews; do not infer live backend support, calibration, timing, or noise behavior.
---

# Qiskit circuit contract reviewer

Review the circuit as a program description whose meaning depends on declared bit conventions and an execution contract. Keep the circuit object, mathematical model, execution request, and returned data separate.

## Required context

Request or identify:

- the Qiskit version;
- the complete circuit construction or diagram;
- the ordered qubit and classical-bit collections;
- every measurement mapping;
- the requested execution interface and options;
- the selected backend or `Target`, if hardware compatibility is in scope;
- the comparison rule and tolerance, if equivalence is claimed.

Report missing material as unresolved rather than supplying assumptions silently.

## Review

1. List operations in program order with public circuit indices obtained through `QuantumCircuit.find_bit` when code is available.
2. Build an ordering ledger covering circuit-list order, diagram order, integer significance, ket labels, Pauli labels, and displayed classical strings that are relevant to the supplied program.
3. Separate unitary preparation from measurement, reset, delay, and control-flow operations.
4. State which mathematical model is being used. Do not describe a `QuantumCircuit` object as a stored state vector.
5. Check the execution interface:
   - exact statevector inspection requires a compatible circuit without measurement or unresolved control flow;
   - a Sampler circuit must expose classical measurement data;
   - an Estimator request must pair the circuit with compatible observables;
   - a local statevector primitive does not model device noise or provide error mitigation merely because it uses the primitive interface.
6. Trace dependencies on each wire and distinguish instruction count, circuit depth, scheduled duration, and wall-clock job time.
7. For parameterized circuits, list free parameters, binding shapes, and the parameter values associated with each result.
8. For compilation claims, require an explicit backend or `Target`. Record operation support, connectivity, layout, optimization level, transpiler seed, and SDK version.
9. Check equivalence with a method that accounts for the declared layout and global phase. Matching one input histogram is insufficient evidence of operator equivalence.
10. For mid-circuit measurement and classical control, identify every branch, the classical condition, the state-changing operation in each branch, and whether the selected execution system supports the control-flow construct.

## Output

Return:

- the declared contract and unresolved assumptions;
- an ordering ledger;
- an operation and measurement trace;
- the selected execution model and interface-fit findings;
- dependency and depth findings;
- compilation metadata and target checks when supplied;
- equivalence evidence at the requested level;
- the smallest reproducible correction for each defect.

## Boundaries

- Do not retrieve a backend or contact a service unless the user authorizes that separate action.
- Do not infer current hardware properties from a vendor, backend family, or historical example.
- Do not convert circuit depth into time without instruction durations and a scheduling model.
- Do not interpret a count-string position until the classical registers and display convention are known.
- Do not treat measurements, resets, control flow, or noise as unitary gates.
- Do not claim that a passing local simulation certifies a physical implementation.
