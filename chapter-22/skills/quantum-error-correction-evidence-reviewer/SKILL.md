---
name: quantum-error-correction-evidence-reviewer
description: Review quantum error-correction code specifications, syndrome records, decoder evidence, distance-scaling studies, and fault-tolerance claims. Use when auditing a QEC manuscript, notebook, experiment bundle, simulator result, hardware report, or QuantumGridOS integration. Do not use it to authenticate, submit hardware jobs, change live decoder settings, or apply device corrections.
---

# Quantum Error-Correction Evidence Reviewer

Review the supplied material as an algebraic code definition, an inference pipeline, and an evidence claim. Preserve unknowns and keep simulator, synthetic-noise, and hardware evidence separate.

## 1. Establish scope and authority

Identify supplied code definitions, circuits, mappings, syndrome data, noise or calibration records, decoders, logical results, comparators, and claims. State whether the review is source-only, simulation-backed, recorded-hardware-backed, or supported by a complete reproducibility bundle.

Default to read-only work. Do not authenticate, submit, cancel, rerun, recalibrate, modify live decoder weights, change device configuration, apply physical recovery, or spend provider credits without separate explicit authorization.

## 2. Validate the code contract

Record n, k, declared distance, stabilizer generators, logical operators, boundaries, and supported error set. Check generator commutation, independence, logical commutation relationships, and any claimed X- and Z-distances. Distinguish a code-space definition from a fault-tolerant extraction circuit.

## 3. Reconstruct the six-stage loop

Create sections for encode, noise, syndrome extraction, decoding, frame update or physical recovery, and logical validation. For each stage, link the supplied artifact and mark absent details unknown.

## 4. Review syndrome and decoder evidence

Keep raw syndrome bits, detection events, decoder hypotheses, recoveries, frame updates, and logical outcomes as separate records. State the decoder's noise assumptions, information boundary, calibration source, version, latency, and treatment of boundaries, leakage, correlations, and measurement faults.

## 5. Classify the claim

Assign at most one highest supported rung: syndrome detection, corrected observable, break-even memory, repeated protected operation, below-threshold scaling, fault-tolerant logical operation, or validated logical algorithm. Postselection must be explicit and cannot be reported as deterministic correction.

Do not establish below-threshold behavior from one physical gate-error number. Require comparable increasing-distance experiments with a fixed task, circuit family, decoder contract, statistical method, and documented changes.

## 6. Check reproducibility and statistics

Require hashes or immutable references for code, scheduled circuits, noise and calibration records, raw syndrome batches, decoder configuration, logical results, and analysis. Record sample counts, accepted and rejected runs, uncertainty intervals, drift treatment, and comparator identity.

## 7. Produce the review

Return:

1. authority and evidence scope;
2. validated code contract and algebraic failures;
3. six-stage reliability map;
4. decoder and information-boundary findings;
5. highest supported evidence rung;
6. unsupported or overstated conclusions;
7. reproducibility and statistical gaps;
8. bounded corrected conclusion;
9. safe read-only next checks;
10. state-changing actions that require separate authorization.
