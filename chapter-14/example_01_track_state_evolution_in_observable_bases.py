import numpy as np
from scipy.linalg import expm


X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
ket_0 = np.array([1, 0], dtype=complex)


def expectation(state, observable):
    return float(np.real(state.conj() @ observable @ state))


object_record = {
    "hamiltonian": "X",
    "initial_state": "|0>",
    "units": "hbar=1",
}
representation_record = {
    "basis_order": "|0>, |1>",
    "state": "complex vector of length 2",
}
transformation_record = {"map": "U(t)=exp(-iXt)", "method": "matrix exponential"}

rows = []
for time in [0.0, np.pi / 4, np.pi / 2, np.pi]:
    unitary = expm(-1j * X * time)
    state = unitary @ ket_0
    row = {
        "t_over_pi": time / np.pi,
        "p0": float(abs(state[0]) ** 2),
        "p1": float(abs(state[1]) ** 2),
        "x": expectation(state, X),
        "y": expectation(state, Y),
        "z": expectation(state, Z),
        "norm": float(np.vdot(state, state).real),
    }
    rows.append(row)

assert np.isclose(rows[1]["p0"], 0.5)
assert np.isclose(rows[1]["p1"], 0.5)
assert np.isclose(rows[2]["p1"], 1.0)
assert np.isclose(rows[3]["p0"], 1.0)
assert all(np.isclose(row["norm"], 1.0) for row in rows)

invariant_record = {
    "unitary": bool(np.allclose(expm(-1j * X).conj().T @ expm(-1j * X), np.eye(2))),
    "norm_preserved": True,
    "timing_check": "equal probabilities at t=pi/4; |1> at t=pi/2",
}

print(f"object_record={object_record}")
print(f"representation_record={representation_record}")
print(f"transformation_record={transformation_record}")
for row in rows:
    print(row)
print(f"invariant_record={invariant_record}")
