"""Trace parity-check extraction without measuring the logical amplitudes."""

from __future__ import annotations

from math import sqrt


State = dict[str, complex]


def apply_x(state: State, qubit: int) -> State:
    """Apply X using the printed order q0 q1 q2 a01 a12."""
    changed: State = {}
    for bits, amplitude in state.items():
        output = list(bits)
        output[qubit] = "0" if output[qubit] == "1" else "1"
        changed["".join(output)] = amplitude
    return changed


def apply_cnot(state: State, control: int, target: int) -> State:
    """Apply a CNOT in the same printed bit order."""
    changed: State = {}
    for bits, amplitude in state.items():
        output = list(bits)
        if output[control] == "1":
            output[target] = "0" if output[target] == "1" else "1"
        changed["".join(output)] = amplitude
    return changed


def extract_syndrome(state: State) -> State:
    """Write q0 XOR q1 into a01 and q1 XOR q2 into a12."""
    for control, target in ((0, 3), (1, 3), (1, 4), (2, 4)):
        state = apply_cnot(state, control, target)
    return state


alpha = sqrt(3) / 2
beta = 0.5j
encoded: State = {"00000": alpha, "11100": beta}

expected = {
    "no error": "00",
    "X on q0": "10",
    "X on q1": "11",
    "X on q2": "01",
}

for label, error_qubit in (
    ("no error", None),
    ("X on q0", 0),
    ("X on q1", 1),
    ("X on q2", 2),
):
    noisy = encoded if error_qubit is None else apply_x(encoded, error_qubit)
    extracted = extract_syndrome(noisy)
    ancilla_values = {bits[3:] for bits in extracted}

    # Both logical branches produce the same syndrome, so measuring the
    # ancillas does not distinguish alpha from beta in these four cases.
    assert ancilla_values == {expected[label]}
    assert sorted(abs(value) for value in extracted.values()) == sorted(
        (abs(alpha), abs(beta))
    )
    print(f"{label:10s} -> syndrome {ancilla_values.pop()} -> {sorted(extracted)}")
