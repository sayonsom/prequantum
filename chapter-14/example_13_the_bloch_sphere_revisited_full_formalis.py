"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.6 The Bloch Sphere Revisited: Full Formalism
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_13_the_bloch_sphere_revisited_full_formalis.py
"""

import numpy as np

# Pauli matrices
I = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)

def bloch_vector(rho):
    """Extract the Bloch vector (r_x, r_y, r_z) from a density matrix."""
    r_x = np.trace(rho @ sigma_x).real
    r_y = np.trace(rho @ sigma_y).real
    r_z = np.trace(rho @ sigma_z).real
    return np.array([r_x, r_y, r_z])

def density_from_bloch(r):
    """Build a density matrix from a Bloch vector."""
    return (I + r[0]*sigma_x + r[1]*sigma_y + r[2]*sigma_z) / 2

# Test with known states
states = {
    "|0⟩": np.outer([1, 0], [1, 0]),
    "|1⟩": np.outer([0, 1], [0, 1]),
    "|+⟩": np.outer([1, 1], [1, 1]) / 2,
    "|−⟩": np.outer([1, -1], [1, -1]) / 2,
    "mixed (50/50)": np.eye(2) / 2,
    "70% |0⟩": 0.7 * np.outer([1, 0], [1, 0]) + 0.3 * np.outer([0, 1], [0, 1]),
}

print(f"{'State':<16} {'r_x':>6} {'r_y':>6} {'r_z':>6} {'|r|':>6} {'Pure?':>6}")
print("-" * 52)
for name, rho in states.items():
    r = bloch_vector(rho)
    length = np.linalg.norm(r)
    pure = "Yes" if np.isclose(length, 1.0) else "No"
    print(f"{name:<16} {r[0]:6.3f} {r[1]:6.3f} {r[2]:6.3f} {length:6.3f} {pure:>6}")

# Verify round-trip: Bloch vector → density matrix → Bloch vector
r_test = np.array([0.0, 0.0, 1.0])  # should be |0⟩
rho_test = density_from_bloch(r_test)
r_back = bloch_vector(rho_test)
print(f"\nRound-trip test: {r_test} → ρ → {r_back}")
print(f"Match: {np.allclose(r_test, r_back)}")
# Output:
# State            r_x    r_y    r_z    |r|  Pure?
# ----------------------------------------------------
# |0⟩              0.000  0.000  1.000  1.000    Yes
# |1⟩              0.000  0.000 -1.000  1.000    Yes
# |+⟩              1.000  0.000  0.000  1.000    Yes
# |−⟩             -1.000  0.000  0.000  1.000    Yes
# mixed (50/50)    0.000  0.000  0.000  0.000     No
# 70% |0⟩          0.000  0.000  0.400  0.400     No
#
# Round-trip test: [0. 0. 1.] → ρ → [0. 0. 1.]
# Match: True
