import numpy as np


def density_report(rho, tolerance=1e-12):
    eigenvalues = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    positive = bool(np.min(eigenvalues) >= -tolerance)
    hermitian = bool(np.allclose(rho, rho.conj().T, atol=tolerance))
    unit_trace = bool(np.isclose(np.trace(rho), 1.0, atol=tolerance))
    purity = float(np.real(np.trace(rho @ rho)))
    nonzero = eigenvalues[eigenvalues > tolerance]
    entropy = float(-np.sum(nonzero * np.log2(nonzero))) if positive and unit_trace else None
    return {
        "hermitian": hermitian,
        "positive_semidefinite": positive,
        "unit_trace": unit_trace,
        "purity": purity,
        "entropy_bits": entropy,
        "valid": hermitian and positive and unit_trace,
    }


ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
minus = np.array([1, -1], dtype=complex) / np.sqrt(2)

rho_plus = np.outer(plus, plus.conj())
rho_z_ensemble = 0.5 * np.outer(ket_0, ket_0.conj()) + 0.5 * np.outer(ket_1, ket_1.conj())
rho_x_ensemble = 0.5 * np.outer(plus, plus.conj()) + 0.5 * np.outer(minus, minus.conj())
rho_invalid = np.array([[0.5, 0.6], [0.6, 0.5]], dtype=complex)

assert np.allclose(rho_z_ensemble, rho_x_ensemble)
assert density_report(rho_plus)["valid"]
assert np.isclose(density_report(rho_plus)["purity"], 1.0)
assert np.isclose(density_report(rho_z_ensemble)["purity"], 0.5)
assert density_report(rho_invalid)["valid"] is False

for name, rho in {
    "pure_plus": rho_plus,
    "maximally_mixed_from_Z_ensemble": rho_z_ensemble,
    "same_matrix_from_X_ensemble": rho_x_ensemble,
    "invalid_negative_eigenvalue": rho_invalid,
}.items():
    print(f"{name}={density_report(rho)}")

print("interpretation=different preparation ensembles can define the same operational density matrix")
