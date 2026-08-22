---
name: quantum-claim-evidence-reviewer
description: Review a supplied quantum-computing claim and its source material using explicit problem, method, execution, baseline, and evidence-level checks. Use when comparing a research result, hardware announcement, roadmap, or application claim. Do not use to invent missing benchmark data or to verify a source that has not been supplied.
---

# Quantum claim evidence reviewer

## Required input

- The exact claim.
- The source material or source links supplied by the user.
- The decision the review is intended to inform.

## Review procedure

1. State the problem input, output, constraints, and success metric.
2. Identify the quantum method and every stated classical component.
3. Classify execution as analytical, simulated, or physical hardware.
4. Record target, compilation, sampling, mitigation, and post-processing details that are present.
5. Name the classical baseline and determine whether the comparison metric and scope match.
6. Assign the highest supported evidence level: correctness, hardware, benchmark, end to end, or operational value.
7. Separate observed results, author interpretations, assumptions, and future targets.
8. State the strongest supported conclusion and list the evidence required for any stronger conclusion.

## Output

Return a concise evidence table, a corrected literal claim, a missing-evidence checklist, and a source list. Mark unavailable information as “not supplied”; do not guess.

## Boundaries

- Do not treat a roadmap as completed capability.
- Do not treat simulator output as hardware evidence.
- Do not infer performance from qubit count alone.
- Do not call a device benchmark an application advantage without an end-to-end comparison.
- Do not accept an unnamed or obsolete classical method as a sufficient baseline.
