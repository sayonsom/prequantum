---
name: quantum-noise-experiment-reviewer
description: Review a quantum circuit noise experiment by separating the ideal circuit, noise model, observation procedure, and evidence. Use when diagnosing unexpected counts, auditing an Aer NoiseModel, checking T1/T2 or readout conventions, or choosing a bounded suppression or mitigation experiment.
---

# Quantum Noise Experiment Reviewer

Review the experiment as four separate records before proposing a remedy.

## 1. Record the ideal contract

- Identify the ideal state, distribution, or observable.
- State which outcomes are permitted and which are unexpected.
- Check circuit order, measurement basis, classical-bit order, and layout.
- Do not use the word fidelity for a simple success-outcome fraction unless that equality has been established for the experiment.

## 2. Record the noise contract

- List every channel, its parameters, its units, and the operations or qubits to which it is attached.
- Label every parameter as measured, fitted, or illustrative.
- For thermal relaxation, require positive times and check `T2 <= 2*T1`.
- For a readout matrix, state explicitly whether columns or rows represent prepared states.
- Confirm that transpiled instruction names match the instructions covered by the noise model.
- Treat depolarizing, Pauli, and independent readout models as bounded approximations. Do not imply that they automatically include leakage, crosstalk, drift, correlated errors, or memory effects.

## 3. Record the observation contract

- Record the shot count, random seeds, observable, basis rotations, and post-processing.
- Separate sampling variation from modeled physical noise.
- Check normalization and uncertainty.
- Prefer a paired ideal/noisy or before/after comparison with only one changed variable.

## 4. Record the evidence contract

- Distinguish an observed symptom from its possible causes.
- Ask what additional experiment would distinguish competing explanations.
- Do not infer a physical mechanism from counts alone.
- If calibration data may drift, request a timestamp or a live backend query.

## 5. Choose the smallest useful intervention

Classify each intervention as circuit/layout improvement, suppression, mitigation, or correction. State the targeted error, assumption, overhead, validation check, and failure condition. Do not promise that mitigation improves every workload.

## Output

Return:

1. a four-record audit;
2. blocking correctness issues;
3. a ranked list of controlled comparisons;
4. a bounded intervention recommendation;
5. unresolved evidence gaps.
