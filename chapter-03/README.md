# Chapter 03: Entanglement and Quantum States

These are the exact copyable artifacts printed in the revised Chapter 3 of *Pre Quantum: Quantum Computing for Software Developers*. Each fenced block in the manuscript links to its corresponding file in this directory.

## Python examples

| # | File | Learning purpose |
|---|---|---|
| 1 | [example_01_two_qubit_basis.py](./example_01_two_qubit_basis.py) | Declare the chapter's left-to-right label and tensor-factor convention. |
| 2 | [example_02_create_bell_state.py](./example_02_create_bell_state.py) | Create Bell Phi-plus and separate amplitudes from probabilities. |
| 3 | [example_03_tensor_product.py](./example_03_tensor_product.py) | Compare `np.kron` with the four manual amplitude products. |
| 4 | [example_04_lift_single_qubit_gate.py](./example_04_lift_single_qubit_gate.py) | Apply X to either position with an identity factor. |
| 5 | [example_05_cnot_truth_table.py](./example_05_cnot_truth_table.py) | Verify the controlled-NOT mapping and unitary invariant. |
| 6 | [example_06_bell_construction.py](./example_06_bell_construction.py) | Inspect every intermediate state in the Bell construction. |
| 7 | [example_07_test_separability.py](./example_07_test_separability.py) | Scope and apply the determinant test for two-qubit pure states. |
| 8 | [example_08_compare_measurement_bases.py](./example_08_compare_measurement_bases.py) | Distinguish Bell Phi-plus from a particular classical correlated mixture. |
| 9 | [example_09_four_bell_states.py](./example_09_four_bell_states.py) | Separate Bell-state amplitude phase from current-basis probabilities. |
| 10 | [example_10_partial_measurement.py](./example_10_partial_measurement.py) | Condition a joint state on one local result and preserve the no-signalling boundary. |

## AI learning prompts

- [Walk through Bell construction](./prompts/01_walk_through_bell_construction.txt)
- [Debug a false entanglement claim](./prompts/02_debug_false_entanglement_claim.txt)
- [Compare joint-state models](./prompts/03_compare_joint_state_models.txt)

## Skill design artifact

- [Two-qubit state reviewer Skill](./skills/two-qubit-state-reviewer/SKILL.md)

Chapter 3 implements a local Skill because the first task is a repeatable review of arrays and claims supplied by the learner. A later MCP can add current backend data, remote job records, calibration context, or maintained benchmark evidence when those external resources are actually required.

## Running the current examples

Install NumPy from the repository root, then run any example directly:

```bash
python -m pip install -r requirements.txt
python chapter-03/example_01_two_qubit_basis.py
```

The earlier automatically extracted Chapter 3 files remain in this directory for repository history and are not the copyable blocks used by the revised chapter.
