# Chapter 19: Quantum Cryptography and Post-Quantum Security

These are the exact companion artifacts for the provisionally revised Chapter
19 of *Pre Quantum: Quantum Computing for Software Developers*.

## Python examples

| Example | Artifact | Purpose |
| --- | --- | --- |
| 19.1 | `example_01_audit_factoring_and_period_finding.py` | Separate trial factoring, exhaustive order finding, and Shor post-processing. |
| 19.2 | `example_02_prepare_measure_and_sift_bb84.py` | Model the ideal prepare, measure, and sift portion of BB84. |
| Circuit Lab 19.1 | `example_09_read_compile_and_trace_a_bb84_signal.py` | Derive, exhaustively verify, transpile, and sample the ideal one-signal BB84 circuit contract. |
| 19.3 | `example_03_measure_intercept_resend_qber.py` | Estimate intercept-resend QBER with confidence intervals. |
| 19.4 | `example_04_calculate_sampling_detection_probability.py` | Calculate the probability that a revealed sample detects errors. |
| 19.5 | `example_05_verify_toy_lwe_correctness.py` | Inspect modular noise and decoding in an insecure toy LWE construction. |
| 19.6 | `example_06_validate_a_standards_registry.py` | Distinguish final NIST standards from selected algorithms. |
| 19.7 | `example_07_prioritize_a_cryptographic_inventory.py` | Prioritize a small inventory without collecting key material. |
| 19.8 | `example_08_build_a_migration_evidence_record.py` | Build a hash-addressed, non-authorizing migration evidence record. |

## AI-practice artifacts

- `prompts/01_explain_the_five_security_records.txt`
- `prompts/02_break_this_audit_a_bb84_claim.txt`
- `prompts/03_translate_pqc_migration_into_typed_interfaces.txt`
- `prompts/04_design_and_trace_a_bb84_signal_circuit.txt`

## Skill artifact

- `skills/cryptographic-migration-evidence-reviewer/SKILL.md`

## Environment used for the chapter audit

- Python 3.14.4
- NumPy 2.4.2
- Qiskit 2.5.2 and Qiskit Aer 0.17.2 for Circuit Lab 19.1
- No production cryptographic library is used by these teaching programs.
- Examples 19.2 through 19.5 are explanatory models and are not suitable for
  creating keys or protecting information.
- Circuit Lab 19.1 is an ideal circuit unit test. It is not a QKD implementation
  and does not establish finite-key, device, or operational security.

Run a local example from this directory with:

```bash
python example_01_audit_factoring_and_period_finding.py
```
