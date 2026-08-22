# Chapter 16: Quantum Optimization

These are the exact companion artifacts for the provisionally revised Chapter 16 of *Pre Quantum: Quantum Computing for Software Developers*.

## Python examples

| Example | Artifact | Purpose |
| --- | --- | --- |
| 16.1 | `example_01_build_and_solve_a_small_qubo.py` | Compile a small generator-selection objective into a QUBO and verify it against the direct objective. |
| 16.2 | `example_02_verify_the_upper_triangular_convention.py` | Enforce the chapter's upper-triangular QUBO storage convention. |
| 16.3 | `example_03_calibrate_an_equality_penalty.py` | Locate the penalty threshold by exact enumeration rather than guesswork. |
| 16.4 | `example_04_convert_qubo_to_ising.py` | Convert every QUBO coefficient to Ising form and verify all assignments. |
| 16.5 | `example_05_run_a_one_layer_qaoa_experiment.py` | Optimize a deterministic one-layer QAOA statevector experiment by grid search. |
| 16.6 | `example_06_verify_an_xy_mixer_preserves_feasibility.py` | Verify that an XY ring mixer preserves Hamming weight. |
| 16.7 | `example_07_wrap_the_model_with_quantumgridos.py` | Wrap the manually verified polynomial in the current QuantumGridOS QUBO interface. |
| 16.8 | `example_08_build_an_optimization_evidence_ledger.py` | Validate a five-record optimization evidence ledger. |

## AI-practice artifacts

- `prompts/01_ask_your_ai_audit_a_qubo_derivation.txt`
- `prompts/02_break_this_find_the_matrix_convention_bug.txt`
- `prompts/03_translate_optimization_into_typed_interfaces.txt`

## Skill artifact

- `skills/qubo-formulation-reviewer/SKILL.md`

## Environment used for the chapter audit

- Python 3.14.4
- NumPy 2.4.2
- SciPy 1.18.1
- Qiskit 2.5.2 for environment provenance; Examples 16.1–16.6 and 16.8 use NumPy/SciPy only.
- Example 16.7 targets QuantumGridOS 0.1.9 at repository commit `dff26bed704886e384c5f7df833828c965a7000a`. It is isolated from the chapter's numerical proof so that the formulation remains auditable without that package.

Run the local examples from this directory with:

```bash
python example_01_build_and_solve_a_small_qubo.py
```
