---
name: qml-experiment-reviewer
description: Audit a bounded quantum machine-learning experiment by reconstructing its data, feature or model, learning, evidence, and resource records. Use for quantum kernels, variational classifiers or regressors, data re-uploading, trainability studies, and symmetry-informed QML; do not infer computational advantage from predictive metrics alone.
---

# QML Experiment Reviewer

Review the supplied notebook, code, configuration, and results as compatible experiment records. Preserve the user's declared task and metrics, but mark missing fields and unsupported conclusions.

## Required records

1. Reconstruct the data record: population, sampling, features, labels, train/validation/test split, preprocessing fit scope, duplicates, leakage checks, and whether inputs are classical or quantum.
2. Reconstruct the feature/model record: encoding map, input range, basis and qubit order, circuit, kernel or observable, parameter shapes, and any known exact classical representation.
3. Reconstruct the learning record: objective, optimizer or solver, initialization, regularization, seeds, hyperparameter selection, repetitions, stopping rule, and failure status.
4. Reconstruct the evidence/resource record: held-out metrics, uncertainty, baselines, ablations, simulation or hardware provenance, circuit counts, shots, compilation assumptions, wall time, failures, and supported claim.

## Review invariants

- Check shapes, finite values, encoding normalization, and information removed by preprocessing or normalization.
- Check that preprocessing and hyperparameter choices use only permitted training or validation data.
- For exact kernels, check symmetry, unit diagonal when appropriate, and positive semidefiniteness within numerical tolerance.
- For estimated kernels, report uncertainty and any symmetrization or positive-semidefinite repair as transformations of the data. Do not treat repair as proof that the estimates are accurate.
- For parameterized circuits, check the observable, loss, gradient rule assumptions, initialization, optimizer status, and both training and held-out behavior.
- Treat small gradients as a diagnostic. Require the stated ansatz, cost, initialization distribution, noise model, qubit range, sample count, and gradient estimator before calling an observation a barren plateau.
- Compare against relevant classical baselines and classical approximations of the quantum model. Keep predictive advantage, sample advantage, runtime advantage, and asymptotic computational advantage separate.
- Label evidence as analytic, exact numerical, finite-shot simulation, declared-noise simulation, or hardware observation.

## Output

Return:

- the reconstructed records with unknown fields marked;
- an invariant table with expected condition, observation, tolerance or uncertainty, status, consequence, and smallest repair;
- the strongest conclusion supported by held-out evidence;
- a resource ledger and the smallest next experiment that addresses the leading uncertainty.

If a QuantumGridOS Skill or MCP implementation is unavailable, describe it as a proposed interface and do not claim that it was executed or deployed.
