# Chapter 18: Quantum Methods for Energy-System Optimization

These are the exact companion artifacts for the provisionally revised Chapter
18 of *Pre Quantum: Quantum Computing for Software Developers*.

## Python examples

| Example | Artifact | Purpose |
| --- | --- | --- |
| 18.1 | `example_01_enumerate_commitment_and_dispatch.py` | Separate binary commitment from continuous economic dispatch. |
| 18.2 | `example_02_verify_a_finite_qubo_encoding.py` | Verify a capacity-selection QUBO over its complete finite state space. |
| 18.3 | `example_03_solve_a_three_period_schedule.py` | Add startup, no-load, and ramp constraints to a small schedule. |
| 18.4 | `example_04_solve_dc_power_flow.py` | Solve and verify a four-bus lossless DC power-flow model. |
| 18.5 | `example_05_run_security_constrained_dispatch.py` | Minimize dispatch cost subject to DC transmission limits. |
| 18.6 | `example_06_screen_commitments_with_a_network_subproblem.py` | Screen binary commitments using a network-constrained LP. |
| 18.7 | `example_07_audit_the_quantumgridos_boundary.py` | Inspect selected interfaces at a pinned QuantumGridOS commit. |
| 18.8 | `example_08_build_an_evidence_record.py` | Build a hash-addressed, read-only evidence record. |

## AI-practice artifacts

- `prompts/01_explain_the_five_energy_records.txt`
- `prompts/02_break_this_audit_an_energy_qubo.txt`
- `prompts/03_translate_grid_optimization_into_typed_interfaces.txt`

## Skill artifact

- `skills/power-system-quantum-workflow-reviewer/SKILL.md`

## Environment used for the chapter audit

- Python 3.14.4
- NumPy 2.4.2
- SciPy 1.18.1
- Example 18.7 targets QuantumGridOS repository commit
  `dff26bed704886e384c5f7df833828c965a7000a`. It performs source inspection
  and does not execute a grid-control or quantum-computing job.

Run a local example from this directory with:

```bash
python example_01_enumerate_commitment_and_dispatch.py
```
