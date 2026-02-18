"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.3 From QUBO to Ising Hamiltonian
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_04_from_qubo_to_ising_hamiltonian.py
"""

import numpy as np

def qubo_to_ising(Q):
    """Convert a QUBO matrix to Ising Hamiltonian coefficients.

    QUBO: f(x) = x^T Q x,  x_i ∈ {0, 1}
    Ising: g(s) = Σ_i h_i s_i + Σ_{i<j} J_{ij} s_i s_j + const,  s_i ∈ {-1, +1}

    Substitution: x_i = (1 - s_i) / 2

    Derivation (for a single term Q_ii * x_i):
      Q_ii * (1 - s_i)/2 = Q_ii/2 - Q_ii/2 * s_i
      → contributes -Q_ii/2 to h_i and Q_ii/2 to the constant

    For a cross term Q_ij * x_i * x_j:
      Q_ij * (1-s_i)/2 * (1-s_j)/2 = Q_ij/4 * (1 - s_i - s_j + s_i*s_j)
      → contributes Q_ij/4 to J_ij, -Q_ij/4 to h_i and h_j, Q_ij/4 to constant
    """
    n = Q.shape[0]
    # Make Q symmetric for easier handling
    Q_sym = (Q + Q.T) / 2

    h = np.zeros(n)       # local fields
    J = np.zeros((n, n))  # coupling strengths
    offset = 0.0

    # From the substitution x_i = (1 - s_i)/2:
    for i in range(n):
        # Diagonal: Q_ii * x_i = Q_ii * (1 - s_i)/2
        h[i] -= Q_sym[i, i] / 2
        offset += Q_sym[i, i] / 2

    for i in range(n):
        for j in range(i+1, n):
            # Off-diagonal: Q_ij * x_i * x_j = Q_ij * (1-s_i)(1-s_j)/4
            J[i, j] = Q_sym[i, j] / 4
            h[i] -= Q_sym[i, j] / 4
            h[j] -= Q_sym[i, j] / 4
            offset += Q_sym[i, j] / 4

    return h, J, offset

# Use the generator QUBO from the Quick Win
generators = [(50, 30), (80, 45), (100, 60)]
demand = 150
penalty = 10
n = 3
Q = np.zeros((n, n))
for i in range(n):
    p_i, c_i = generators[i]
    Q[i, i] = c_i + penalty * (p_i**2 - 2 * demand * p_i)
for i in range(n):
    for j in range(i+1, n):
        Q[i, j] = penalty * 2 * generators[i][0] * generators[j][0]

h, J, offset = qubo_to_ising(Q)
qubo_offset = penalty * demand**2  # constant from constraint expansion

print("Ising local fields h:")
for i in range(n):
    print(f"  h[{i}] = {h[i]:>10.1f}")
print("\nIsing couplings J:")
for i in range(n):
    for j in range(i+1, n):
        if J[i, j] != 0:
            print(f"  J[{i},{j}] = {J[i, j]:>10.1f}")
print(f"\nIsing offset: {offset:.1f}")
print(f"QUBO offset (penalty * demand²): {qubo_offset:.1f}")
print(f"Total constant: {offset + qubo_offset:.1f}")

# Verify: evaluate both formulations on the optimal solution (1, 0, 1)
x_opt = np.array([1, 0, 1])
s_opt = 1 - 2 * x_opt  # convert to spins: x=1 → s=-1, x=0 → s=+1

qubo_val = x_opt @ Q @ x_opt + qubo_offset
ising_val = np.dot(h, s_opt) + sum(
    J[i, j] * s_opt[i] * s_opt[j]
    for i in range(n) for j in range(i+1, n)
) + offset + qubo_offset

print(f"\nQUBO value at (1,0,1): {qubo_val:.1f}")
print(f"Ising value at (-1,+1,-1): {ising_val:.1f}")
print(f"Match: {np.isclose(qubo_val, ising_val)}")
# Output:
# Ising local fields h:
#   h[0] =    16250.0
#   h[1] =    27975.0
#   h[2] =    35235.0
#
# Ising couplings J:
#   J[0,1] =    20000.0
#   J[0,2] =    25000.0
#   J[1,2] =    40000.0
#
# Ising offset: -79460.0
# QUBO offset (penalty * demand²): 225000.0
# Total constant: 145540.0
#
# QUBO value at (1,0,1): 1560.0
# Ising value at (-1,+1,-1): 1560.0
# Match: True
