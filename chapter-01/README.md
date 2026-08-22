# Chapter 01: Why Quantum, Why Now?

These are the exact copyable artifacts printed in Chapter 1 of *Pre Quantum: Quantum Computing for Software Developers*. Each fenced block in the manuscript links to its corresponding file in this directory.

## Python examples

| # | File | Learning purpose |
|---|---|---|
| 1 | [example_01_review_claim.py](./example_01_review_claim.py) | Classify a quantum-computing statement by the kind of evidence it provides. |
| 2 | [example_02_execution_boundary.py](./example_02_execution_boundary.py) | Keep circuit construction separate from the simulator or QPU that executes it. |

## AI learning prompts

- [Review a quantum claim](./prompts/01_review_quantum_claim.txt)
- [Break a claim into category errors](./prompts/02_break_claim_category_errors.txt)
- [Translate a quantum workflow](./prompts/03_translate_quantum_workflow.txt)

## Skill design artifact

- [Quantum claim evidence reviewer Skill](./skills/quantum-claim-evidence-reviewer/SKILL.md)

Chapter 1 uses a local Skill because the task is a repeatable reasoning procedure over text that the reader supplies. A later MCP can add live access to provider documentation, papers, and benchmark records when the workflow needs authenticated or changing external evidence.

## Running the Python examples

The examples use only the Python standard library and can be run directly from the repository root:

```bash
python chapter-01/example_01_review_claim.py
python chapter-01/example_02_execution_boundary.py
```
