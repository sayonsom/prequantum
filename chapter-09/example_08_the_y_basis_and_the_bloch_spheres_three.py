"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.5 The Y-Basis and the Bloch Sphere's Three Axes
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_08_the_y_basis_and_the_bloch_spheres_three.py
"""

import numpy as np

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
ket_minus = (ket_0 - ket_1) / np.sqrt(2)
ket_plus_i = (ket_0 + 1j * ket_1) / np.sqrt(2)
ket_minus_i = (ket_0 - 1j * ket_1) / np.sqrt(2)

# A state tilted toward |1⟩ with a phase
theta = np.pi / 3  # 60 degrees from |0⟩
psi = np.cos(theta/2) * ket_0 + np.exp(1j * np.pi/4) * np.sin(theta/2) * ket_1
print(f"|ψ⟩ = {np.round(psi, 4)}")

# Z-basis measurement probabilities
pZ_0 = abs(np.dot(ket_0.conj(), psi))**2
pZ_1 = abs(np.dot(ket_1.conj(), psi))**2
print(f"\nZ-basis: P(|0⟩)={pZ_0:.4f}, P(|1⟩)={pZ_1:.4f}")

# X-basis measurement probabilities
pX_plus  = abs(np.dot(ket_plus.conj(), psi))**2
pX_minus = abs(np.dot(ket_minus.conj(), psi))**2
print(f"X-basis: P(|+⟩)={pX_plus:.4f}, P(|−⟩)={pX_minus:.4f}")

# Y-basis measurement probabilities
pY_plus  = abs(np.dot(ket_plus_i.conj(), psi))**2
pY_minus = abs(np.dot(ket_minus_i.conj(), psi))**2
print(f"Y-basis: P(|+i⟩)={pY_plus:.4f}, P(|−i⟩)={pY_minus:.4f}")

# Each basis reveals different information about the state.
# You need ALL THREE to fully reconstruct the Bloch sphere position.
# Z tells you the polar angle, X and Y together tell you the azimuthal phase.
