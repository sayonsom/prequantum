# Chapter 20 executable artifacts

These examples were tested with Python 3.14.4, NumPy 2.4.2, Qiskit 2.5.2, Qiskit Aer 0.17.2, Cirq Core 1.7.0, and PennyLane 0.45.1. They use local simulators, reproducible fake targets, or synthetic records only. None authenticates to a cloud service, discovers a live backend, or submits a hardware job.

Run every example from the repository root with:

```text
python code/chapter-20/example_01_compare_three_sdk_contracts.py
python code/chapter-20/example_02_separate_exact_probabilities_from_shots.py
python code/chapter-20/example_03_compile_against_a_backend_target.py
python code/chapter-20/example_04_audit_stochastic_compilation.py
python code/chapter-20/example_05_compare_sampler_and_estimator.py
python code/chapter-20/example_06_validate_a_hardware_run_plan.py
python code/chapter-20/example_07_analyze_a_finite_shot_record.py
python code/chapter-20/example_08_apply_bounded_readout_mitigation.py
python code/chapter-20/example_09_read_a_transpilation_record.py
```

The `prompts/` directory contains the four copy-ready AI labs from the chapter. The `skills/quantum-experiment-evidence-reviewer/` directory contains the reusable read-only Skill. A companion Skill and local MCP plugin are available in the QuantumGridOS repository at `plugins/quantumgridos-hardware-evidence`; its packaged records are explicitly synthetic teaching fixtures, not provider or physical-QPU evidence.
