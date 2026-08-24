# Chapter 21 executable artifacts

These examples use the Python standard library and synthetic records only. They do not start a network service, authenticate to a provider, submit a quantum job, spend credits, or mutate external state.

Run every example from the repository root with:

```text
python code/chapter-21/example_01_trace_the_nested_execution_stack.py
python code/chapter-21/example_02_build_a_service_request_record.py
python code/chapter-21/example_03_run_a_durable_job_state_machine.py
python code/chapter-21/example_04_enforce_idempotent_submission.py
python code/chapter-21/example_05_reconcile_an_uncertain_submission.py
python code/chapter-21/example_06_cache_only_identical_evidence.py
python code/chapter-21/example_07_normalize_provider_job_snapshots.py
python code/chapter-21/example_08_build_low_cardinality_service_metrics.py
python code/chapter-21/example_09_review_a_quantumgridos_adapter_plan.py
```

The four copyable AI prompts are in `code/chapter-21/prompts/`. The reusable local review Skill is in `code/chapter-21/skills/quantum-service-architecture-reviewer/`. Every artifact is read-only and provider-neutral; the QuantumGridOS repository contains the separately packaged evidence-review plugin described in the chapter.
