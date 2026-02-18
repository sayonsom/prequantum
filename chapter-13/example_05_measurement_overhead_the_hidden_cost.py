"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.4 Measurement Overhead: The Hidden Cost
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_05_measurement_overhead_the_hidden_cost.py
"""

import numpy as np

# H = -ZZ - 0.5 XI - 0.5 IX + 0.3 YY has 4 Pauli terms.
# But ZZ and YY can't be measured simultaneously (they don't commute
# on the same qubits in the same basis). So you need multiple
# measurement circuits.

# Grouping commuting terms: terms that share a measurement basis
# can be measured in one circuit.
# Group 1: ZZ (measure both qubits in Z basis)
# Group 2: XI, IX (both involve X, can be co-measured with basis rotations)
# Group 3: YY (measure both in Y basis)
# Total: 3 measurement circuits per VQE iteration.

# Let's simulate shot-based estimation
def estimate_expectation_shots(state, pauli_op_matrix, n_shots):
    """Estimate ⟨ψ|O|ψ⟩ from finite measurements.

    For a Pauli operator, measurement outcomes are ±1.
    The expectation value is the mean of these outcomes.
    """
    # Probability of each computational basis state
    probs = np.abs(state) ** 2

    # For a diagonal operator (like ZZ), eigenvalues are the diagonal
    eigenvalues = np.diag(pauli_op_matrix).real

    # Sample outcomes according to Born rule
    outcomes = np.random.choice(len(probs), size=n_shots, p=probs)
    measured_values = eigenvalues[outcomes]

    return np.mean(measured_values), np.std(measured_values) / np.sqrt(n_shots)

# Example: estimate ⟨ψ|Z⊗Z|ψ⟩ for a Bell state
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
ZZ = np.kron(Z, Z)

exact = np.real(bell.conj() @ ZZ @ bell)
print(f"Exact ⟨Φ+|ZZ|Φ+⟩ = {exact:.4f}")
print(f"\nShot-based estimates:")
for n_shots in [100, 1_000, 10_000, 100_000]:
    est, err = estimate_expectation_shots(bell, ZZ, n_shots)
    print(f"  {n_shots:>7d} shots: {est:.4f} ± {err:.4f}")

# The precision scales as 1/√(shots).
# For ε = 0.01 precision: need ~10,000 shots per Pauli term.
# With 4 Pauli terms × 10,000 shots = 40,000 circuit executions per
# VQE iteration. With 300 iterations → 12 million circuit runs total.
print(f"\nShot scaling: precision ε requires O(1/ε²) shots per term")
print(f"For H with k terms and precision ε:")
print(f"  Total shots per VQE iteration: O(k/ε²)")
print(f"  Total VQE cost: O(k × n_iterations / ε²)")
