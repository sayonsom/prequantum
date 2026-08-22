# Chapter 06: Quantum Circuits

Runnable examples and copyable learning artifacts from *Pre Quantum: Quantum Computing for Software Developers*.

## Guided-learning revision

| # | Artifact | Learning task |
|---|---|---|
| 1 | [example_01_circuit_to_result.py](./example_01_circuit_to_result.py) | Separate the circuit, exact model, sampled execution, and result |
| 2 | [example_02_inspect_circuit_contract.py](./example_02_inspect_circuit_contract.py) | Inspect operations and bit mappings through public APIs |
| 3 | [example_03_qiskit_bit_order.py](./example_03_qiskit_bit_order.py) | Reconcile Qiskit's circuit, ket-label, and count-string conventions |
| 4 | [example_04_execution_contracts.py](./example_04_execution_contracts.py) | Choose exact probabilities or expectation values according to the question |
| 5 | [example_05_depth_and_dependencies.py](./example_05_depth_and_dependencies.py) | Read circuit depth from wire dependencies |
| 6 | [example_06_parameterized_template.py](./example_06_parameterized_template.py) | Compose and bind a parameterized circuit template |
| 7 | [example_07_compile_for_target.py](./example_07_compile_for_target.py) | Compile against an explicit target and verify the transformed circuit |
| 8 | [example_08_dynamic_reset_to_zero.py](./example_08_dynamic_reset_to_zero.py) | Trace mid-circuit measurement and classical feedforward |

The three copyable prompts are stored in [prompts](./prompts/). The reusable local reviewer is stored as the [qiskit-circuit-contract-reviewer Skill](./skills/qiskit-circuit-contract-reviewer/).

These examples were validated with Qiskit 2.5.2 and Qiskit Aer 0.17.2. Install compatible versions with:

```bash
python -m pip install "qiskit~=2.5" "qiskit-aer~=0.17" numpy
```

## Earlier source extraction

The following files are retained as code extracted from the earlier manuscript. The guided-learning revision above is the publication set for the revised chapter.

## Code Files

| # | File | Section |
|---|------|--------|
| 1 | [example_01_the_quick_win.py](./example_01_the_quick_win.py) | The Quick Win |
| 2 | [example_02_anatomy_of_a_quantum_circuit.py](./example_02_anatomy_of_a_quantum_circuit.py) | Anatomy of a Quantum Circuit |
| 3 | [example_03_anatomy_of_a_quantum_circuit.py](./example_03_anatomy_of_a_quantum_circuit.py) | Anatomy of a Quantum Circuit |
| 4 | [example_04_running_circuits_simulators_shots_and_th.py](./example_04_running_circuits_simulators_shots_and_th.py) | Running Circuits: Simulators, Shots, and the Primitives API |
| 5 | [example_05_running_circuits_simulators_shots_and_th.py](./example_05_running_circuits_simulators_shots_and_th.py) | Running Circuits: Simulators, Shots, and the Primitives API |
| 6 | [example_06_running_circuits_simulators_shots_and_th.py](./example_06_running_circuits_simulators_shots_and_th.py) | Running Circuits: Simulators, Shots, and the Primitives API |
| 7 | [example_07_running_circuits_simulators_shots_and_th.py](./example_07_running_circuits_simulators_shots_and_th.py) | Running Circuits: Simulators, Shots, and the Primitives API |
| 8 | [example_08_multi_qubit_circuits_and_the_gate_librar.py](./example_08_multi_qubit_circuits_and_the_gate_librar.py) | Multi-Qubit Circuits and the Gate Library |
| 9 | [example_09_multi_qubit_circuits_and_the_gate_librar.py](./example_09_multi_qubit_circuits_and_the_gate_librar.py) | Multi-Qubit Circuits and the Gate Library |
| 10 | [example_10_multi_qubit_circuits_and_the_gate_librar.py](./example_10_multi_qubit_circuits_and_the_gate_librar.py) | Multi-Qubit Circuits and the Gate Library |
| 11 | [example_11_circuit_depth_why_it_matters.py](./example_11_circuit_depth_why_it_matters.py) | Circuit Depth: Why It Matters |
| 12 | [example_12_circuit_depth_why_it_matters.py](./example_12_circuit_depth_why_it_matters.py) | Circuit Depth: Why It Matters |
| 13 | [example_13_the_dag_how_qiskit_actually_sees_your_ci.py](./example_13_the_dag_how_qiskit_actually_sees_your_ci.py) | The DAG: How Qiskit Actually Sees Your Circuit |
| 14 | [example_14_the_dag_how_qiskit_actually_sees_your_ci.py](./example_14_the_dag_how_qiskit_actually_sees_your_ci.py) | The DAG: How Qiskit Actually Sees Your Circuit |
| 15 | [example_15_transpilation_from_your_circuit_to_the_h.py](./example_15_transpilation_from_your_circuit_to_the_h.py) | Transpilation: From Your Circuit to the Hardware's |
| 16 | [example_16_transpilation_from_your_circuit_to_the_h.py](./example_16_transpilation_from_your_circuit_to_the_h.py) | Transpilation: From Your Circuit to the Hardware's |
| 17 | [example_17_transpilation_from_your_circuit_to_the_h.py](./example_17_transpilation_from_your_circuit_to_the_h.py) | Transpilation: From Your Circuit to the Hardware's |
| 18 | [example_18_transpilation_from_your_circuit_to_the_h.py](./example_18_transpilation_from_your_circuit_to_the_h.py) | Transpilation: From Your Circuit to the Hardware's |
| 19 | [example_19_parameterized_circuits_templates_for_var.py](./example_19_parameterized_circuits_templates_for_var.py) | Parameterized Circuits: Templates for Variational Algorithms |
| 20 | [example_20_parameterized_circuits_templates_for_var.py](./example_20_parameterized_circuits_templates_for_var.py) | Parameterized Circuits: Templates for Variational Algorithms |
| 21 | [example_21_dynamic_circuits_mid_circuit_measurement.py](./example_21_dynamic_circuits_mid_circuit_measurement.py) | Dynamic Circuits: Mid-Circuit Measurement and Classical Feedforward |
| 22 | [example_22_dynamic_circuits_mid_circuit_measurement.py](./example_22_dynamic_circuits_mid_circuit_measurement.py) | Dynamic Circuits: Mid-Circuit Measurement and Classical Feedforward |
| 23 | [example_23_dynamic_circuits_mid_circuit_measurement.py](./example_23_dynamic_circuits_mid_circuit_measurement.py) | Dynamic Circuits: Mid-Circuit Measurement and Classical Feedforward |
| 24 | [example_24_statevector_simulation_seeing_behind_the.py](./example_24_statevector_simulation_seeing_behind_the.py) | Statevector Simulation: Seeing Behind the Curtain |
| 25 | [example_25_statevector_simulation_seeing_behind_the.py](./example_25_statevector_simulation_seeing_behind_the.py) | Statevector Simulation: Seeing Behind the Curtain |
| 26 | [example_26_circuit_composition_and_reuse.py](./example_26_circuit_composition_and_reuse.py) | Circuit Composition and Reuse |
| 27 | [example_27_circuit_composition_and_reuse.py](./example_27_circuit_composition_and_reuse.py) | Circuit Composition and Reuse |
| 28 | [example_28_break_this.py](./example_28_break_this.py) | Break This |
| 29 | [example_29_exercises.py](./example_29_exercises.py) | Exercises |

## Running the guided examples

```bash
python chapter-06/example_01_circuit_to_result.py
python chapter-06/example_02_inspect_circuit_contract.py
python chapter-06/example_03_qiskit_bit_order.py
python chapter-06/example_04_execution_contracts.py
python chapter-06/example_05_depth_and_dependencies.py
python chapter-06/example_06_parameterized_template.py
python chapter-06/example_07_compile_for_target.py
python chapter-06/example_08_dynamic_reset_to_zero.py
```
