"""Connect the X, Y, and Z bases with observable expectation values."""

import numpy as np


x = np.array([[0, 1], [1, 0]], dtype=complex)
y = np.array([[0, -1j], [1j, 0]], dtype=complex)
z = np.array([[1, 0], [0, -1]], dtype=complex)

plus_x = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2)
plus_y = np.array([1.0, 1.0j], dtype=complex) / np.sqrt(2)
plus_z = np.array([1.0, 0.0], dtype=complex)

states = {"+X": plus_x, "+Y": plus_y, "+Z": plus_z}
observables = {"X": x, "Y": y, "Z": z}

for state_name, psi in states.items():
    row = {}
    for observable_name, operator in observables.items():
        row[observable_name] = float(np.vdot(psi, operator @ psi).real)
    print(state_name, row)

assert np.isclose(np.vdot(plus_x, x @ plus_x), 1.0)
assert np.isclose(np.vdot(plus_y, y @ plus_y), 1.0)
assert np.isclose(np.vdot(plus_z, z @ plus_z), 1.0)
assert np.isclose(np.vdot(plus_y, x @ plus_y), 0.0)
assert np.isclose(np.vdot(plus_y, z @ plus_y), 0.0)
