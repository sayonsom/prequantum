---
name: quantum-advantage-evidence-reviewer
description: Review a quantum-computing advantage claim as a typed, versioned evidence ledger and return bounded findings without inventing measurements or changing source artifacts.
---

# Quantum Advantage Evidence Reviewer

Use this Skill when a user asks to review a quantum-versus-classical benchmark, an advantage or utility claim, a proposed pilot, or an evidence bundle. Operate read-only unless the user separately authorizes a specific edit.

## 1. Establish the task contract

Extract the input family, required output, acceptance test, approximation rule, counted resources, and intended user. Mark every absent field as missing. Do not infer a production task from a demonstration task.

## 2. Classify every evidence source

Label each result as mathematical analysis, exact classical computation, stochastic classical simulation, ideal quantum simulation, noisy quantum simulation, emulation, or physical quantum hardware. Preserve the source's date, artifact identity, environment, and limitations. Never promote one evidence type to another.

## 3. Reconstruct both computational paths

For the classical path, record algorithm, implementation, version, tuning, hardware, stopping rule, and validator. For the quantum path, record algorithm or physical procedure, encoding, compilation, hardware or simulator, calibration context, sampling, mitigation, postprocessing, and validator. Identify every stage excluded from resource accounting.

## 4. Test comparison fairness

Compare task fidelity, result quality, resources, scale, access, reproducibility, and usefulness separately. Report mismatched inputs, outputs, tolerances, or accounting boundaries before discussing performance. Treat the classical baseline as versioned software that may change.

## 5. Separate conclusion types

Classify each conclusion as asymptotic, empirical, or practical. State the assumptions and measured region. Reject an inference from one type to another when additional evidence is required.

## 6. Apply an evidence-proportional gate

Recommend only a bounded action such as learn, monitor, reproduce, explore, pilot, or deploy. For pilot or deploy recommendations, require a relevant user outcome, complete resource account, operational owner, security and governance review, independent validation, and explicit stop conditions. If these are absent, return the narrower eligible action.

## 7. Produce the review

Return:

1. a one-sentence narrow claim;
2. evidence present by dimension;
3. evidence missing by dimension;
4. fairness defects;
5. unsupported inferences;
6. the eligible action and its prerequisites;
7. the smallest next test;
8. provenance and limitations.

Do not create data, benchmark results, citations, hardware runs, provider access, financial estimates, or career forecasts. Do not modify source artifacts. Say explicitly when the evidence is insufficient.
