# Chapter 17: Quantum Simulation

These are the exact companion artifacts for the provisionally revised Chapter 17 of *Pre Quantum: Quantum Computing for Software Developers*.

## Python examples

| Example | Artifact | Purpose |
| --- | --- | --- |
| 17.1 | `example_01_evolve_a_two_spin_model_exactly.py` | Evolve a two-qubit transverse-field model and verify norm, symmetry, and energy invariants. |
| 17.2 | `example_02_audit_commuting_and_noncommuting_terms.py` | Compute commutators before selecting a Hamiltonian-splitting method. |
| 17.3 | `example_03_compare_product_formula_errors.py` | Compare first- and symmetric-second-order formulas with an exact operator reference. |
| 17.4 | `example_04_compile_pauli_evolution_blocks.py` | Verify the matrices implemented by one- and two-qubit Pauli-evolution circuit blocks. |
| 17.5 | `example_05_measure_an_observable_with_finite_shots.py` | Separate exact state evolution from a finite-shot observable estimate. |
| 17.6 | `example_06_run_a_qdrift_channel_experiment.py` | Estimate a qDRIFT ensemble channel with reproducible Monte Carlo trials. |
| 17.7 | `example_07_inspect_an_h2_qubit_hamiltonian.py` | Reconstruct and inspect a fixed two-qubit molecular Hamiltonian. |
| 17.8 | `example_08_audit_the_quantumgridos_solver_boundary.py` | Classify the current QuantumGridOS HHL-fast numerical and circuit paths. |

## AI-practice artifacts

- `prompts/01_explain_the_simulation_records.txt`
- `prompts/02_break_this_find_the_missing_term.txt`
- `prompts/03_translate_simulation_into_typed_interfaces.txt`

## Skill artifact

- `skills/hamiltonian-simulation-reviewer/SKILL.md`

## Environment used for the chapter audit

- Python 3.14.4
- NumPy 2.4.2
- SciPy 1.18.1
- Qiskit 2.5.2 for environment provenance; the chapter examples use NumPy and SciPy directly.
- Example 17.8 targets QuantumGridOS 0.1.9 at repository commit `dff26bed704886e384c5f7df833828c965a7000a`. It records that the reviewed `hhl_fast` path returns a classical NumPy solution together with a proof-of-concept circuit.

Run the local examples from this directory with:

```bash
python example_01_evolve_a_two_spin_model_exactly.py
```
