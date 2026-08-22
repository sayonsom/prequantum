# Chapter 02: Classical Bits to Qubits

These are the exact copyable artifacts printed in Chapter 2 of *Pre Quantum: Quantum Computing for Software Developers*. Each fenced block in the manuscript links to its corresponding file in this directory.

## Python examples

| # | File | Learning purpose |
|---|---|---|
| 1 | [example_01_hadamard_twice.py](./example_01_hadamard_twice.py) | Predict and verify a two-Hadamard round trip. |
| 2 | [example_02_classical_bit.py](./example_02_classical_bit.py) | Contrast a non-mutating classical read with qubit measurement. |
| 3 | [example_03_state_probabilities.py](./example_03_state_probabilities.py) | Convert amplitudes to standard-basis probabilities. |
| 4 | [example_04_normalize_state.py](./example_04_normalize_state.py) | Treat normalization as a checked state invariant. |
| 5 | [example_05_standard_basis_measurement.py](./example_05_standard_basis_measurement.py) | Separate fresh preparation from repeated measurement. |
| 6 | [example_06_hadamard_relative_signs.py](./example_06_hadamard_relative_signs.py) | Observe why relative amplitude signs affect interference. |
| 7 | [example_07_hadamard_round_trip.py](./example_07_hadamard_round_trip.py) | Reconstruct the Hadamard self-inverse property. |
| 8 | [example_08_qiskit_hadamard_measurement.py](./example_08_qiskit_hadamard_measurement.py) | Map an equal-amplitude state to a Qiskit simulation. |
| 9 | [example_09_qiskit_hadamard_round_trip.py](./example_09_qiskit_hadamard_round_trip.py) | Verify the two-Hadamard result in Qiskit. |
| 10 | [example_10_debug_normalization.py](./example_10_debug_normalization.py) | Diagnose an intentionally incorrect normalization. |

## AI learning prompts

- [Hadamard worked example](./prompts/01_hadamard_worked_example.txt)
- [Debug normalization](./prompts/02_debug_normalization.txt)
- [Translate the measurement model](./prompts/03_translate_measurement_model.txt)

## Skill and MCP design artifacts

- [Single-qubit state reviewer Skill](./skills/single-qubit-state-reviewer/SKILL.md)
- [Single-qubit state analysis MCP schema](./mcp/analyze_single_qubit_state.schema.json)

## Running the Python examples

Install the chapter dependencies from the repository root, then run any example directly:

```bash
python -m pip install -r requirements.txt
python chapter-02/example_01_hadamard_twice.py
```

Examples 8 and 9 require `qiskit` and `qiskit-aer`. The remaining examples require NumPy.
