# Chapter 13: Variational Quantum Algorithms

These artifacts support the revised Chapter 13 manuscript. Each Python file is
a standalone, deterministic experiment with assertions. The prompt files and
local Skill are copied exactly into the manuscript.

## Python examples

1. `example_01_run_a_bounded_variational_loop.py`
2. `example_02_separate_the_variational_bound_from_an_estimator.py`
3. `example_03_compare_reachable_state_families.py`
4. `example_04_run_a_reproducible_vqe.py`
5. `example_05_estimate_pauli_terms_with_finite_shots.py`
6. `example_06_map_and_solve_a_small_maxcut_qaoa.py`
7. `example_07_measure_gradient_statistics_carefully.py`
8. `example_08_label_a_variational_evidence_ledger.py`

## AI learning artifacts

- `prompts/01_audit_a_variational_algorithm_claim.txt`
- `prompts/02_break_a_vqe_or_qaoa_pipeline.txt`
- `prompts/03_translate_variational_workflows_into_data_interfaces.txt`
- `skills/variational-run-reviewer/SKILL.md`

The examples require NumPy, SciPy, and Qiskit. Run one with
`python example_01_run_a_bounded_variational_loop.py`.
