"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.3 The General Phase Gate: Rz(θ)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_07_the_general_phase_gate_rzθ.py
"""

import numpy as np

def Rz(theta):
    """Rotation gate around the z-axis by angle theta."""
    return np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)]
    ], dtype=complex)

# Rz is the generalization of all phase gates
# (up to a global phase factor, which doesn't affect measurement)
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Demonstrate different rotation angles
for angle_name, theta in [("π/4 (≈T)", np.pi/4), ("π/2 (≈S)", np.pi/2),
                            ("π (≈Z)", np.pi), ("π/8", np.pi/8)]:
    gate = Rz(theta)
    result = gate @ ket_1
    print(f"  Rz({angle_name:10s})|1⟩ = {np.round(result, 4)}")

# Verify: Rz(π) ≈ Z (up to global phase)
# Global phase: e^(-iπ/2) = -i, so Rz(π) = -i·Z
print(f"\nRz(π) = -iZ? {np.allclose(Rz(np.pi), -1j * np.array([[1,0],[0,-1]]))}")
