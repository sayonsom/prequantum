---
name: quantum-service-architecture-reviewer
description: Review a quantum-classical service by separating request, plan, job, result, and operations records and mapping nested execution loops. Use when designing or auditing asynchronous APIs, shots, algorithm iterations, polling, retries, idempotency, provider adapters, result caches, observability, or QuantumGridOS service boundaries. Do not use it to authenticate, submit, cancel, or mutate provider jobs.
---

# Quantum Service Architecture Reviewer

Review the supplied design as a distributed system and as a quantum-evidence pipeline. Preserve unknowns instead of filling them with plausible provider behavior.

## 1. Establish scope and authority

Identify the service boundary, callers, provider adapters, persistence systems, workers, result stores, and application validators that are actually supplied. State whether the review is source-only, configuration-only, record-based, or supported by execution evidence.

Default to read-only work. Do not authenticate, submit, cancel, rerun, reserve capacity, rotate credentials, change production configuration, or spend provider credits without separate explicit authorization.

## 2. Build the five-record ledger

Create separate sections for:

- **Request record:** service request ID, tenant or authorization reference, idempotency key, intent hash, requested evidence contract, backend-selection policy, creation time, and schema version.
- **Plan record:** capability snapshot, compilation hash, execution mode, provider and region scope, budget or quota policy, retry policy, result destination, and approval reference.
- **Job record:** service job ID, provider job ID when known, append-only state transitions, submission attempts, reconciliation state, timestamps, and terminal reason.
- **Result record:** immutable raw result reference, provider metadata, evidence class, uncertainty, derived transformations, application validation, and provenance hashes.
- **Operations record:** traces, low-cardinality metrics, structured logs, cache decisions, retry counts, incidents, redaction state, and service-version information.

Mark every absent field `unknown` or `not supplied`. Never put tokens, passwords, private keys, or provider credentials into these records.

## 3. Map nested execution and repetition

Create a loop ledger for every supplied repetition boundary. For each boundary, record the repeated object, owner, input, output, stopping rule, authoritative record, and whether it creates new quantum evidence. Check explicitly for Python construction loops, compiler candidate search, shot repetition, provider jobs, batch or session grouping, classical optimizer updates, provider polling, service retry or reconciliation, and complete experiment replication.

Keep the following distinctions explicit:

- a gate is one circuit instruction;
- a circuit is one ordered preparation, transformation, and measurement description;
- a shot is one fresh preparation and execution of the same compiled circuit;
- a provider job is a scheduled unit with a provider lifecycle;
- a classical iteration may bind new parameters and create new quantum work;
- polling changes service knowledge but does not create quantum evidence;
- retry or reconciliation is an operational decision and must not silently become experiment replication.

## 4. Check distributed-system invariants

Verify that:

- a repeated idempotency key with the same request hash returns the same service job;
- reusing that key with different input produces a conflict;
- an immutable plan is stored before provider submission;
- an ambiguous submission outcome is reconciled before another submission attempt;
- service job state and provider state remain separate but linked;
- terminal transitions cannot silently return to a running state;
- workers can restart without losing authoritative job state;
- cache identity includes every field that defines the evidence;
- raw results remain immutable when derived results are recalculated;
- authorization to inspect a record is distinct from authorization to submit or cancel work.

Report an invariant failure as an error, not as provider noise.

## 5. Check quantum evidence boundaries

Distinguish exact simulation, finite-shot ideal simulation, noisy or synthetic data, provider simulator jobs, and physical-QPU jobs. A successful HTTP request, worker completion, provider job, or cache hit does not by itself prove scientific validity, application feasibility, optimality, or quantum advantage.

Require the result record to link back to the exact intent, capability, compilation, and execution evidence needed for the stated conclusion.

## 6. Review deployment and operations

Check container provenance, dependency pins, non-root execution, external secret handling, least privilege, bounded retries, timeout ownership, durable storage, result retention, trace correlation, metric-cardinality limits, health semantics, and incident visibility.

Treat product names, plan limits, queue policies, pricing, device availability, and managed-service interfaces as time-sensitive. Require a dated primary source or mark the claim for re-verification.

## 7. Produce the review

Return:

1. architecture and authority scope;
2. five-record ledger;
3. nested execution and loop ledger;
4. passed and failed invariants;
5. duplicate-work and data-loss risks;
6. unsupported quantum or application claims;
7. deployment, secret, and observability findings;
8. bounded corrected conclusions;
9. safe read-only next checks;
10. state-changing actions that require separate authorization.
