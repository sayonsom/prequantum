# Chapter 23 learning artifacts

This directory contains the exact executable examples, AI learning prompts, and read-only review Skill printed in Chapter 23, “From Quantum Claims to Engineering Decisions.”

The nine examples use only the Python standard library. They build solver-independent problem contracts, classical baselines, evidence records, validators, decision gates, portfolio manifests, and one circuit-to-decision plan. They do not execute a quantum circuit, call a provider, or provide hardware evidence.

Run all examples from this directory with:

```bash
for file in example_*.py; do python "$file"; done
```

The `prompts/` directory contains the exact four copyable prompts. The `skills/quantum-advantage-evidence-reviewer/` directory contains the exact read-only Skill artifact printed in the chapter.
