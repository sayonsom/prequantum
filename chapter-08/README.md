# Chapter 8: Quantum Information Essentials

These artifacts support the revised Chapter 8 manuscript. Each Python file is a standalone learning example with assertions. The prompt files and local Skill are copied exactly into the manuscript.

## Python examples

1. `example_01_test_a_basis_label_copier.py`
2. `example_02_prove_no_cloning_with_inner_products.py`
3. `example_03_trace_teleportation_branches.py`
4. `example_04_verify_dynamic_teleportation.py`
5. `example_05_check_no_signalling.py`
6. `example_06_run_superdense_coding.py`
7. `example_07_compare_fidelity_and_trace_distance.py`
8. `example_08_test_global_phase_in_superdense_coding.py`

## AI learning artifacts

- `prompts/01_trace_a_teleportation_protocol.txt`
- `prompts/02_audit_quantum_resource_accounting.txt`
- `prompts/03_review_a_state_similarity_claim.txt`
- `skills/quantum-information-protocol-reviewer/SKILL.md`

The examples use explicit semantic names for phase and flip bits. Qiskit count strings are displayed in descending classical-bit order, so the superdense-coding example parses the display before comparing it with the semantic message.
