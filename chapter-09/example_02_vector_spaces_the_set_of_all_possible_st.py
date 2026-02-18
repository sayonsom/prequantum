"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.1 Vector Spaces: The Set of All Possible States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_02_vector_spaces_the_set_of_all_possible_st.py
"""

import numpy as np

# Qubit states are vectors in C² (2D complex vector space)
state_a = np.array([0.6+0j, 0.8+0j])
state_b = np.array([0.8+0j, -0.6+0j])

# CLOSURE UNDER ADDITION: adding two vectors gives another vector
raw_sum = state_a + state_b
# But we need to renormalize for it to be a valid quantum state
normalized_sum = raw_sum / np.linalg.norm(raw_sum)
print(f"a + b (normalized): {np.round(normalized_sum, 4)}")

# CLOSURE UNDER SCALAR MULTIPLICATION: scaling a vector gives another vector
scaled = (0.5 + 0.5j) * state_a
scaled_normalized = scaled / np.linalg.norm(scaled)
print(f"Scaled a (normalized): {np.round(scaled_normalized, 4)}")

# THE ZERO VECTOR exists: np.array([0, 0])
zero = np.zeros(2, dtype=complex)
print(f"Zero vector: {zero}")

# DIMENSION: C² has dimension 2. Two basis vectors span the whole space.
# ANY qubit state can be written as α|0⟩ + β|1⟩ for some α, β.
basis_0 = np.array([1, 0], dtype=complex)  # |0⟩
basis_1 = np.array([0, 1], dtype=complex)  # |1⟩

alpha, beta = 0.6, 0.8
reconstructed = alpha * basis_0 + beta * basis_1
print(f"\n0.6|0⟩ + 0.8|1⟩ = {reconstructed}")
print(f"Same as state_a?  {np.allclose(reconstructed, state_a)}")  # True
