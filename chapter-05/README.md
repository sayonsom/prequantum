# Chapter 05: Quantum Gates as Transformations

Runnable examples and copyable learning artifacts from *Pre Quantum: Quantum Computing for Software Developers*.

## Guided-learning revision

| # | Artifact | Learning task |
|---|---|---|
| 1 | [example_01_phase_to_probability.py](./example_01_phase_to_probability.py) | Trace relative phase into a measurement probability |
| 2 | [example_02_pauli_contracts.py](./example_02_pauli_contracts.py) | Reconstruct the Pauli gate contracts |
| 3 | [example_03_phase_family.py](./example_03_phase_family.py) | Distinguish phase gates, rotations, and controlled phase |
| 4 | [example_04_hadamard_and_order.py](./example_04_hadamard_and_order.py) | Review basis change and application order |
| 5 | [example_05_validate_unitary.py](./example_05_validate_unitary.py) | Validate a deterministic closed-system gate |
| 6 | [example_06_multi_qubit_gates.py](./example_06_multi_qubit_gates.py) | Verify CNOT, SWAP, and Toffoli behavior |
| 7 | [example_07_exact_gate_identities.py](./example_07_exact_gate_identities.py) | Separate exact identities from approximate synthesis |
| 8 | [example_08_target_decomposition.py](./example_08_target_decomposition.py) | Check an illustrative target decomposition |

The three book prompts are stored in [prompts](./prompts/). The reusable local reviewer is stored as the [quantum-gate-sequence-reviewer Skill](./skills/quantum-gate-sequence-reviewer/).

## Earlier source extraction

The following files are retained as the code extracted from the earlier manuscript. The guided-learning revision above is the publication set for the revised chapter.

| # | File | Section |
|---|------|--------|
| 1 | [example_01_the_quick_win.py](./example_01_the_quick_win.py) | The Quick Win |
| 2 | [example_02_the_pauli_gates_x_y_z.py](./example_02_the_pauli_gates_x_y_z.py) | The Pauli Gates: X, Y, Z |
| 3 | [example_03_the_pauli_gates_x_y_z.py](./example_03_the_pauli_gates_x_y_z.py) | The Pauli Gates: X, Y, Z |
| 4 | [example_04_the_pauli_gates_x_y_z.py](./example_04_the_pauli_gates_x_y_z.py) | The Pauli Gates: X, Y, Z |
| 5 | [example_05_phase_gates_s_and_t.py](./example_05_phase_gates_s_and_t.py) | Phase Gates: S and T |
| 6 | [example_06_phase_gates_s_and_t.py](./example_06_phase_gates_s_and_t.py) | Phase Gates: S and T |
| 7 | [example_07_the_general_phase_gate_rzθ.py](./example_07_the_general_phase_gate_rzθ.py) | The General Phase Gate: Rz(θ) |
| 8 | [example_08_the_general_phase_gate_rzθ.py](./example_08_the_general_phase_gate_rzθ.py) | The General Phase Gate: Rz(θ) |
| 9 | [example_09_the_hadamard_revisited_basis_change.py](./example_09_the_hadamard_revisited_basis_change.py) | The Hadamard Revisited: Basis Change |
| 10 | [example_10_gate_composition_and_the_order_trap.py](./example_10_gate_composition_and_the_order_trap.py) | Gate Composition and the Order Trap |
| 11 | [example_11_the_unitary_constraint_what_makes_a_vali.py](./example_11_the_unitary_constraint_what_makes_a_vali.py) | The Unitary Constraint: What Makes a Valid Gate |
| 12 | [example_12_the_unitary_constraint_what_makes_a_vali.py](./example_12_the_unitary_constraint_what_makes_a_vali.py) | The Unitary Constraint: What Makes a Valid Gate |
| 13 | [example_13_multi_qubit_gates_cnot_toffoli_swap.py](./example_13_multi_qubit_gates_cnot_toffoli_swap.py) | Multi-Qubit Gates: CNOT, Toffoli, SWAP |
| 14 | [example_14_multi_qubit_gates_cnot_toffoli_swap.py](./example_14_multi_qubit_gates_cnot_toffoli_swap.py) | Multi-Qubit Gates: CNOT, Toffoli, SWAP |
| 15 | [example_15_multi_qubit_gates_cnot_toffoli_swap.py](./example_15_multi_qubit_gates_cnot_toffoli_swap.py) | Multi-Qubit Gates: CNOT, Toffoli, SWAP |
| 16 | [example_16_universality_building_anything_from_a_fe.py](./example_16_universality_building_anything_from_a_fe.py) | Universality: Building Anything from a Few Gates |
| 17 | [example_17_universality_building_anything_from_a_fe.py](./example_17_universality_building_anything_from_a_fe.py) | Universality: Building Anything from a Few Gates |
| 18 | [example_18_native_gates_what_real_hardware_actually.py](./example_18_native_gates_what_real_hardware_actually.py) | Native Gates: What Real Hardware Actually Uses |
| 19 | [example_19_putting_it_all_together_the_gate_landsca.py](./example_19_putting_it_all_together_the_gate_landsca.py) | Putting It All Together: The Gate Landscape |
| 20 | [example_20_break_this.py](./example_20_break_this.py) | Break This |

## Running the Code

```bash
pip install qiskit qiskit-aer numpy matplotlib
python <filename>.py
```
