# Chapter 11: Grover Search and Amplitude Amplification

These artifacts support the revised Chapter 11 manuscript. Each Python file is a standalone experiment with assertions. The prompt files and local Skill are copied exactly into the manuscript.

## Python examples

1. `example_01_run_a_bounded_grover_experiment.py`
2. `example_02_verify_a_phase_marking_oracle.py`
3. `example_03_test_the_diffusion_reflection.py`
4. `example_04_choose_a_finite_iteration_count.py`
5. `example_05_search_when_the_marked_count_is_unknown.py`
6. `example_06_amplify_a_nonuniform_preparation.py`
7. `example_07_audit_a_qiskit_query_ledger.py`
8. `example_08_bound_a_synthetic_noise_result.py`

## AI learning artifacts

- `prompts/01_audit_a_grover_search_claim.txt`
- `prompts/02_break_an_iteration_query_or_shot_ledger.txt`
- `prompts/03_translate_two_reflections_into_a_rotation.txt`
- `skills/grover-amplitude-amplification-reviewer/SKILL.md`

The examples require NumPy, Qiskit, and Qiskit Aer. Run one with `python example_01_run_a_bounded_grover_experiment.py`.
