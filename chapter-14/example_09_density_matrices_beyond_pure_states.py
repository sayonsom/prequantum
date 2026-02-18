"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.3 Density Matrices: Beyond Pure States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_09_density_matrices_beyond_pure_states.py
"""

import numpy as np

def von_neumann_entropy(rho):
    """Compute S(ρ) = -Tr(ρ log₂ ρ) via eigenvalues."""
    eigenvalues = np.linalg.eigvalsh(rho)
    # Filter out zero eigenvalues (0 log 0 = 0 by convention)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    return -np.sum(eigenvalues * np.log2(eigenvalues))

# Test on various states
ket_0 = np.array([1, 0], dtype=complex)
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)

states = {
    "Pure |0⟩":        np.outer(ket_0, ket_0.conj()),
    "Pure |+⟩":        np.outer(plus, plus.conj()),
    "Mixed 70/30":     0.7 * np.diag([1, 0]).astype(complex) + 0.3 * np.diag([0, 1]).astype(complex),
    "Maximally mixed": np.eye(2, dtype=complex) / 2,
}

print(f"{'State':<20} {'Purity':>8} {'Entropy':>8}")
print("-" * 40)
for name, rho in states.items():
    purity = np.trace(rho @ rho).real
    entropy = von_neumann_entropy(rho)
    print(f"{name:<20} {purity:8.4f} {entropy:8.4f}")
# Output:
# State                  Purity  Entropy
# ----------------------------------------
# Pure |0⟩               1.0000   0.0000
# Pure |+⟩               1.0000   0.0000
# Mixed 70/30            0.5800   0.8813
# Maximally mixed        0.5000   1.0000
