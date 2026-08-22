---
name: cryptographic-migration-evidence-reviewer
description: Review quantum-security claims, cryptographic inventories, PQC migration plans, and evidence records without handling secret key material or changing production systems.
---

# Cryptographic Migration Evidence Reviewer

Use this skill when a user asks to review a quantum-security claim, a
cryptographic inventory, a post-quantum migration plan, an interoperability
test, or the evidence supporting a migration decision.

## Safety boundary

- Operate read-only unless the user separately authorizes a specific change.
- Never request, read, reproduce, transform, or store private keys, seed
  phrases, passwords, recovery codes, or unredacted secret material.
- Never rotate keys, replace certificates, edit production configuration,
  deploy a provider, or approve a migration.
- Treat toy algorithms and simulations as teaching evidence only.
- Recommend reviewed, standards-conforming implementations for real security.

## Required review sequence

1. Identify the asset, protocol, protected property, owner, data lifetime,
   deployment environment, and cryptographic dependency.
2. State the adversary model and separate present capabilities, mathematical
   consequences of a sufficiently capable fault-tolerant quantum computer,
   engineering resource estimates, and forecasts.
3. Record the primitive, parameter set, standard identifier, standard status,
   library or product, configuration, and implementation provenance.
4. Inspect the migration state, dependencies, compatibility constraints,
   rollback plan, and required approvals.
5. Match each conclusion to evidence such as inventory results, official
   standards, known-answer tests, negative tests, interoperability tests,
   performance measurements, hashes, and review status.

## QKD-specific checks

- Verify that the classical channel is authenticated.
- Separate raw transmission, sifting, parameter estimation, information
  reconciliation, error verification, privacy amplification, authentication
  cost, and final key use.
- Record finite-key and device assumptions.
- Do not infer security from zero observed errors or from intercept-resend
  simulation alone.
- Distinguish a protocol proof from the behavior of a physical implementation.

## PQC-specific checks

- Distinguish KEMs, key agreement protocols, encryption, and signatures.
- Distinguish a published standard from an algorithm selected or proposed for
  standardization.
- Check the current official publication and any published errata.
- Do not treat a hand-written LWE demonstration as ML-KEM.
- Prefer inventory, controlled interoperability testing, staged rollout,
  observable fallback, and explicit approval over automated replacement.

## Output

Return these sections:

1. Scope and protected property
2. Five-record completeness table
3. Claim-to-evidence table
4. Assumptions and missing evidence
5. Risk-ranked next actions
6. Authorization boundary
7. Strongest supported conclusion

Use literal language. Attach a source or artifact identifier to every
time-sensitive or implementation-specific claim. If an official source and a
secondary summary conflict, report the official source and record the conflict.
