import numpy as np


I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho_plus = np.outer(plus, plus.conj())


def apply_channel(rho, operators):
    return sum(operator @ rho @ operator.conj().T for operator in operators)


def complete(operators):
    return np.allclose(sum(operator.conj().T @ operator for operator in operators), I)


def bloch_vector(rho):
    return np.array([np.trace(rho @ pauli).real for pauli in (X, Y, Z)])


def phase_flip(probability):
    return [np.sqrt(1 - probability) * I, np.sqrt(probability) * Z]


def dephasing(strength):
    # Off-diagonal entries are multiplied by 1-strength.
    return [np.sqrt(1 - strength / 2) * I, np.sqrt(strength / 2) * Z]


def depolarizing(strength):
    return [
        np.sqrt(1 - 3 * strength / 4) * I,
        np.sqrt(strength / 4) * X,
        np.sqrt(strength / 4) * Y,
        np.sqrt(strength / 4) * Z,
    ]


def amplitude_damping(probability):
    return [
        np.array([[1, 0], [0, np.sqrt(1 - probability)]], dtype=complex),
        np.array([[0, np.sqrt(probability)], [0, 0]], dtype=complex),
    ]


channels = {
    "phase_flip_p=1": phase_flip(1.0),
    "complete_dephasing_g=1": dephasing(1.0),
    "complete_depolarizing_p=1": depolarizing(1.0),
    "amplitude_damping_g=1": amplitude_damping(1.0),
}

outputs = {}
for name, operators in channels.items():
    assert complete(operators)
    output = apply_channel(rho_plus, operators)
    outputs[name] = output
    print(f"{name}: bloch={np.round(bloch_vector(output), 6)}, rho={np.round(output, 6)}")

assert np.allclose(bloch_vector(outputs["phase_flip_p=1"]), [-1, 0, 0])
assert np.allclose(bloch_vector(outputs["complete_dephasing_g=1"]), [0, 0, 0])
assert np.allclose(outputs["complete_depolarizing_p=1"], I / 2)
assert np.allclose(outputs["amplitude_damping_g=1"], np.array([[1, 0], [0, 0]]))
print("interpretation=a certain phase flip is unitary; complete dephasing removes coherence")
