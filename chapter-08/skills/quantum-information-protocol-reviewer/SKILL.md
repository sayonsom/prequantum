---
name: quantum-information-protocol-reviewer
description: Review no-cloning, teleportation, superdense-coding, and state-comparison work through explicit state, ownership, resource, and evidence ledgers. Use when checking a quantum communication circuit, classical feedforward, bit ordering, no-signalling, fidelity, trace distance, or claims about what a protocol transmits or proves.
---

# Quantum Information Protocol Reviewer

Review the protocol through four separate ledgers before accepting its conclusion.

## 1. State ledger

- Identify every initial state and its tensor-factor order.
- Distinguish an arbitrary unknown state from a known preparation recipe.
- Record each unitary, measurement branch, conditional state, and discarded subsystem.
- Treat equality up to global phase as physical-state equivalence.
- Do not treat equal probabilities in one basis as equality of quantum states.

## 2. Ownership ledger

- Record who holds each system before and after every operation or transmission.
- Distinguish moving a physical carrier from transferring a state using prior entanglement and classical feedforward.
- For teleportation, confirm that Alice's message system is not retained as an independent copy.
- For superdense coding, identify the qubit Alice physically transmits to Bob.

## 3. Resource ledger

- Count pre-shared ebits, transmitted qubits, transmitted classical bits, measurements, and consumed entanglement.
- State when the entangled resource must have been distributed.
- Confirm that Bob cannot decode teleportation before the classical message arrives.
- Confirm that superdense coding does not claim two classical bits from one unassisted qubit channel.
- Record assumptions about noise, authentication, timing, and dynamic-circuit support.

## 4. Evidence ledger

- Match every claim to the observation that supports it.
- Require more than computational-basis probabilities when relative phase matters.
- Use an inverse-preparation check, tomography, or a justified fidelity protocol for full-state evidence.
- Parse SDK bit-string display order separately from semantic message order.
- Distinguish exact statevector or density-matrix calculations from finite-shot estimates.
- For equal-prior binary discrimination, use success probability `(1 + D) / 2`, where `D` is trace distance.

## Protocol-specific checks

### No-cloning

- State the input family. Copying known orthogonal labels does not provide a universal cloner.
- Use linearity or preservation of inner products to test the claim.
- Do not infer that every form of state preparation or broadcasting is forbidden.

### Teleportation

- Produce all four measurement branches and their corrections.
- Verify the correction-bit mapping against the circuit's classical registers.
- Check Bob's reduced state before the classical bits arrive; it must not encode a usable message about the input.

### Superdense coding

- Name the two semantic message bits by their actions, such as phase bit and flip bit.
- Verify all four encodings and the decoder.
- Treat `ZX` and `XZ` as differing by global phase in this use; do not report a decoding difference from that phase alone.

### State comparison

- Confirm normalization and valid density-matrix invariants.
- State the fidelity convention. Qiskit's state fidelity uses the squared convention.
- Check trace distance and the Fuchs-van de Graaf bounds.
- Do not calculate quantum-state fidelity from a single measurement distribution without a protocol that establishes the connection.

## Output

Return:

1. the four ledgers;
2. blocking correctness issues;
3. a branch and bit-order audit;
4. a minimal verification experiment;
5. the strongest supported conclusion; and
6. unresolved evidence gaps.
