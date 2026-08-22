# Chapter 7: Noise and Errors

These artifacts support the revised Chapter 7 manuscript. Each Python file is a standalone, deterministic learning example. The prompt files and local Skill are copied exactly into the manuscript.

## Python examples

1. `example_01_compare_ideal_and_noisy_counts.py`
2. `example_02_inspect_error_visibility.py`
3. `example_03_measure_t1_t2_signatures.py`
4. `example_04_compare_coherent_and_stochastic_error.py`
5. `example_05_track_density_matrix_purity.py`
6. `example_06_estimate_an_error_budget.py`
7. `example_07_calibrate_readout_error.py`
8. `example_08_extrapolate_to_zero_noise.py`

## AI learning artifacts

- `prompts/01_diagnose_unexpected_counts.txt`
- `prompts/02_audit_a_noise_model.txt`
- `prompts/03_choose_a_noise_strategy.txt`
- `skills/quantum-noise-experiment-reviewer/SKILL.md`

The chapter intentionally does not assign live backend calibration values to named processors. Device properties drift and should be inspected at execution time through a backend `Target` or a future live-data MCP.
