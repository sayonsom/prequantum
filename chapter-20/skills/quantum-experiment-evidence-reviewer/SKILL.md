---
name: quantum-experiment-evidence-reviewer
description: Review quantum SDK, transpilation, backend, job, result, and hardware claims by separating five evidence records and reading logical-to-physical mappings. Use when auditing a quantum experiment, explaining a source-to-ISA transformation, distinguishing repetition scopes, diagnosing a simulator-to-hardware discrepancy, checking reproducibility, or designing a read-only backend/job inspection workflow. Do not use it to submit, cancel, or mutate provider jobs.
---

# Quantum Experiment Evidence Reviewer

Review the supplied experiment through five records. Preserve unknowns instead of filling them with plausible values.

## 1. Establish the evidence class

Classify each supplied result as one of:

1. exact analytical or statevector output;
2. finite-shot ideal simulation;
3. noisy simulation or mock-backend output;
4. provider simulator job;
5. physical-QPU job.

Do not promote evidence from one class to another. A backend-like interface is not proof of physical execution.

## 2. Build the five-record ledger

Create separate sections for:

- **Intent record:** mathematical task, circuit or circuit hash, parameters, measurement or observable contract, shots or target precision, expected invariants, and classical comparator.
- **Capability record:** provider, backend identifier, inspection timestamp, operational state, target operations, connectivity, qubit count, relevant limits, and calibration identifier or timestamp when available.
- **Compilation record:** input hash, target snapshot reference, output hash, layout, operations, depth, two-qubit count, optimization settings, approximation settings, and transpiler seed.
- **Execution record:** primitive or provider interface, job identifier, submission and completion times, run options, shots or precision, status, and result-location reference. Never include credentials.
- **Evidence record:** raw values, metadata, uncertainty, mitigation or post-processing steps, validation results, comparison baseline, and bounded interpretation.

Mark every absent field `unknown` or `not supplied`.

## 3. Read logical-to-ISA transpilation

When source and compiled circuits are supplied, read the transformation in four passes:

1. **Intent:** identify logical wires, preparation, entangling operations, measurements or observables, classical register order, and the declared output invariant.
2. **Layout:** reconstruct initial logical-to-physical placement, routing-induced final placement, workspace or ancilla positions, and the physical-measurement-to-classical-bit map.
3. **ISA:** verify native operations and physical edges against the recorded target. Report depth and native two-qubit count. Do not search for source gate names inside valid decompositions.
4. **Evidence:** define an exact behavioral check for declared inputs when tractable, followed by a separate finite-shot decoding check. State what each test does and does not prove.

Never infer a layout, bit order, or measurement map from visual wire order alone. Mark it `unknown` when the compilation record does not supply it.

## 4. Distinguish repetition scopes

Classify every loop or repetition as one of:

- a Python construction loop that appends operations and produces one source circuit;
- a compiler candidate loop that varies declared seeds or settings and selects one ISA circuit;
- shots inside one job that repeat one measurement request and aggregate one result record;
- experiment repetitions that refresh some or all records and must remain separate until pooling is justified.

A provider queue changes waiting time. It is not an algorithmic loop. For every repetition, name the repeated object, stopping rule, output artifact, and owning record.

## 5. Check cross-record invariants

Verify that:

- the intent fits the recorded backend capacity;
- the compiled circuit uses only operations and connectivity allowed by the target snapshot;
- the compiled observable follows the final qubit layout;
- the execution refers to the exact compiled artifact and options;
- shot totals or estimator precision agree with the returned data;
- post-processing is reproducible from the preserved raw result;
- any claimed application conclusion is checked by an independent domain validator.

Report a mismatch as an error, not as ordinary noise.

## 6. Audit causal claims

Reject conclusions such as “mitigation worked,” “hardware found the optimum,” or “the algorithm is noise resilient” unless the evidence includes an appropriate baseline, repeated or otherwise justified uncertainty analysis, and a comparison that isolates the claimed cause. Agreement with one classical answer is not enough.

Distinguish:

- execution success from scientific validity;
- a lower error metric from an unbiased estimator;
- a feasible decoded candidate from an optimal solution;
- current backend status from historical execution conditions;
- provider metadata from author inference.

## 7. Respect operational boundaries

Default to read-only work: inspect local artifacts, validate schemas, compare hashes, and analyze supplied result records. Do not authenticate, submit, cancel, rerun, reserve, or spend provider credits unless the user explicitly authorizes that separate operation and supplies its scope.

Never request that credentials be pasted into a prompt, manuscript, log, or evidence record. Refer to provider-supported credential storage instead.

## 8. Produce the review

Return:

1. evidence-class determination;
2. five-record ledger;
3. four-pass transpilation audit when applicable;
4. repetition-scope classification when applicable;
5. passed and failed invariants;
6. unsupported claims;
7. corrected bounded conclusions;
8. missing evidence required for a stronger conclusion;
9. safe next checks, separated from any state-changing operation.
