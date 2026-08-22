"""Test Deutsch-Jozsa classification and its promise boundary."""

import numpy as np


def hadamard_power(width):
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    result = np.array([[1.0]], dtype=complex)
    for _ in range(width):
        result = np.kron(result, h)
    return result


def run_phase_query(values):
    size = len(values)
    width = int(np.log2(size))
    transform = hadamard_power(width)
    zero_state = np.eye(size, dtype=complex)[:, 0]
    phase_oracle = np.diag([(-1) ** value for value in values])
    return transform @ phase_oracle @ transform @ zero_state


promised_cases = {
    "constant zero": [0] * 8,
    "constant one": [1] * 8,
    "balanced parity": [bin(x).count("1") % 2 for x in range(8)],
}

for name, values in promised_cases.items():
    amplitudes = run_phase_query(values)
    probability_zero = abs(amplitudes[0]) ** 2
    verdict = "constant" if np.isclose(probability_zero, 1.0) else "balanced"
    print(f"{name:16s} p(000)={probability_zero:.3f} verdict={verdict}")
    assert verdict == ("constant" if name.startswith("constant") else "balanced")

# The algorithm has no required behavior outside the constant-or-balanced promise.
unpromised = [0, 0, 0, 0, 0, 0, 0, 1]
probability_zero = abs(run_phase_query(unpromised)[0]) ** 2
print(f"unpromised input p(000)={probability_zero:.3f}; no valid DJ verdict")
assert 0.0 < probability_zero < 1.0
