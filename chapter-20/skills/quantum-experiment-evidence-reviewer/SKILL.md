---
name: quantum-experiment-evidence-reviewer
description: Review quantum SDK, compilation, backend, job, result, and hardware claims by separating five evidence records. Use when auditing a quantum experiment, diagnosing a simulator-to-hardware discrepancy, checking reproducibility, or designing a read-only backend/job inspection workflow. Do not use it to submit, cancel, or mutate provider jobs.
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

## 3. Check cross-record invariants

Verify that:

- the intent fits the recorded backend capacity;
- the compiled circuit uses only operations and connectivity allowed by the target snapshot;
- the compiled observable follows the final qubit layout;
- the execution refers to the exact compiled artifact and options;
- shot totals or estimator precision agree with the returned data;
- post-processing is reproducible from the preserved raw result;
- any claimed application conclusion is checked by an independent domain validator.

Report a mismatch as an error, not as ordinary noise.

## 4. Audit causal claims

Reject conclusions such as “mitigation worked,” “hardware found the optimum,” or “the algorithm is noise resilient” unless the evidence includes an appropriate baseline, repeated or otherwise justified uncertainty analysis, and a comparison that isolates the claimed cause. Agreement with one classical answer is not enough.

Distinguish:

- execution success from scientific validity;
- a lower error metric from an unbiased estimator;
- a feasible decoded candidate from an optimal solution;
- current backend status from historical execution conditions;
- provider metadata from author inference.

## 5. Respect operational boundaries

Default to read-only work: inspect local artifacts, validate schemas, compare hashes, and analyze supplied result records. Do not authenticate, submit, cancel, rerun, reserve, or spend provider credits unless the user explicitly authorizes that separate operation and supplies its scope.

Never request that credentials be pasted into a prompt, manuscript, log, or evidence record. Refer to provider-supported credential storage instead.

## 6. Produce the review

Return:

1. evidence-class determination;
2. five-record ledger;
3. passed and failed invariants;
4. unsupported claims;
5. corrected bounded conclusions;
6. missing evidence required for a stronger conclusion;
7. safe next checks, separated from any state-changing operation.

