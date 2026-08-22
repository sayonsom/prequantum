# Chapter 04: Reading Quantum Mathematics as a Developer

Code examples from *Pre Quantum: Quantum Computing for Software Developers*.

## Guided-learning artifacts

| # | Artifact | Chapter use |
|---|---|---|
| 1 | [example_01_decode_ket.py](./example_01_decode_ket.py) | Ket, basis order, coordinates, and probabilities |
| 2 | [example_02_braket_and_born_rule.py](./example_02_braket_and_born_rule.py) | Bras, inner products, and the Born rule |
| 3 | [example_03_global_relative_phase.py](./example_03_global_relative_phase.py) | Global phase and relative phase |
| 4 | [example_04_tensor_product.py](./example_04_tensor_product.py) | Tensor products and factorability |
| 5 | [example_05_operator_composition.py](./example_05_operator_composition.py) | Operator order and Bell-state construction |
| 6 | [example_06_unitary_invariant.py](./example_06_unitary_invariant.py) | Full-matrix unitarity checks |
| 7 | [example_07_outer_product_projector.py](./example_07_outer_product_projector.py) | Outer products and projectors |
| 8 | [example_08_shape_ledger.py](./example_08_shape_ledger.py) | Shape-ledger review |
| 9 | [prompts/01_decode_bell_amplitude.txt](./prompts/01_decode_bell_amplitude.txt) | AI lab: decode a composed expression |
| 10 | [prompts/02_debug_inner_outer_product.txt](./prompts/02_debug_inner_outer_product.txt) | AI lab: debug category errors |
| 11 | [prompts/03_model_dirac_types.txt](./prompts/03_model_dirac_types.txt) | AI lab: build a typed mental model |
| 12 | [skills/dirac-notation-translator/SKILL.md](./skills/dirac-notation-translator/SKILL.md) | Reusable notation-review Skill |

The older automatically extracted examples remain in this directory as historical source artifacts. The table above lists the verified artifacts used by the revised chapter.

## Running the Code

Install NumPy, then run any example independently:

```bash
python -m pip install numpy
python example_01_decode_ket.py
```
