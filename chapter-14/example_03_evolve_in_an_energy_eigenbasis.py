import numpy as np
from scipy.linalg import expm


X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)

energies, energy_vectors = np.linalg.eigh(Z)


def evolve_from_spectrum(time):
    phases = np.exp(-1j * energies * time)
    coefficients = energy_vectors.conj().T @ plus
    return energy_vectors @ (phases * coefficients)


def expectation(state, observable):
    return float(np.real(state.conj() @ observable @ state))


for time in [0.0, np.pi / 4, np.pi / 2]:
    spectral_state = evolve_from_spectrum(time)
    direct_state = expm(-1j * Z * time) @ plus
    assert np.allclose(spectral_state, direct_state)
    p_z = np.abs(spectral_state) ** 2
    x_mean = expectation(spectral_state, X)
    y_mean = expectation(spectral_state, Y)
    z_mean = expectation(spectral_state, Z)
    print(
        f"t/pi={time/np.pi:.2f}, pZ={np.round(p_z, 6)}, "
        f"<X>={x_mean:+.6f}, <Y>={y_mean:+.6f}, <Z>={z_mean:+.6f}"
    )

assert np.allclose(np.abs(evolve_from_spectrum(np.pi / 4)) ** 2, [0.5, 0.5])
assert np.isclose(expectation(evolve_from_spectrum(np.pi / 4), Y), 1.0)
print("interpretation=energy-basis populations stay fixed while relative phase changes other observables")
