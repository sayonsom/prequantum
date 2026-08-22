import numpy as np


plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2)
rho_initial = np.outer(plus, plus.conj())
t2 = 120e-6

print("time_us  coherence_factor  purity")

for time in [0.0, 40e-6, 120e-6, 240e-6, 600e-6]:
    coherence_factor = np.exp(-time / t2)
    rho = rho_initial.copy()
    rho[0, 1] *= coherence_factor
    rho[1, 0] *= coherence_factor
    purity = np.trace(rho @ rho).real
    print(f"{time * 1e6:7.1f}  {coherence_factor:16.4f}  {purity:.4f}")

    assert np.isclose(np.trace(rho), 1.0)
    assert np.all(np.linalg.eigvalsh(rho) >= -1e-12)

assert np.isclose(np.trace(rho_initial @ rho_initial).real, 1.0)
