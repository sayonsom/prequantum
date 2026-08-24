---
name: cryptographic-migration-evidence-reviewer
description: Review quantum-security claims, BB84 circuit and protocol boundaries, cryptographic inventories, PQC migration plans, and evidence records without handling secret key material or changing production systems.
---

# Cryptographic Migration Evidence Reviewer

Use this skill when a user asks to review a quantum-security claim, a
cryptographic inventory, a post-quantum migration plan, an interoperability
test, an ideal BB84 circuit claim, or the evidence supporting a migration
decision.

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
6. When a quantum circuit is present, record its classical request fields,
   logical gate order, measurement map, target basis, compilation settings,
   equivalence check, repetition semantics, and the claim that the circuit can
   and cannot support.

## QKD-specific checks

- Verify that the classical channel is authenticated.
- For one ideal BB84 signal, verify the preparation order
  $H^\alpha X^a|0\rangle$, Bob's $H^\beta$ basis change, and the final
  computational-basis measurement.
- Distinguish classical host conditions that construct optional gates from
  coherent controls, dynamic circuit feedback, and authenticated classical
  post-processing.
- Distinguish one fresh protocol signal from repeated simulator shots of one
  fixed circuit request. A measured signal is not reused at another index.
- If a circuit is transpiled, require a declared target, compiler settings,
  operation and measurement mappings, and a checked logical-to-compiled
  relationship.
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
2. Circuit-and-protocol boundary, when applicable
3. Five-record completeness table
4. Claim-to-evidence table
5. Assumptions and missing evidence
6. Risk-ranked next actions
7. Authorization boundary
8. Strongest supported conclusion

Use literal language. Attach a source or artifact identifier to every
time-sensitive or implementation-specific claim. If an official source and a
secondary summary conflict, report the official source and record the conflict.
