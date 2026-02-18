"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.1 The Ket: Vectors Are States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_03_the_ket_vectors_are_states.py
"""

# These are states you've been using for two chapters
state_0 = np.array([1, 0], dtype=complex)
state_1 = np.array([0, 1], dtype=complex)
state_super = np.array([1, 1], dtype=complex) / np.sqrt(2)

# Physicists write them as:
# state_0     → |0⟩    (pronounced "ket zero")
# state_1     → |1⟩    (pronounced "ket one")
# state_super → |+⟩    (pronounced "ket plus")

# Any qubit state: α|0⟩ + β|1⟩ is just alpha * ket_0 + beta * ket_1
alpha, beta = 0.6+0j, 0.8+0j
state = alpha * ket_0 + beta * ket_1
print(f"0.6|0⟩ + 0.8|1⟩ = {state}")    # [0.6+0.j 0.8+0.j]
print(f"|α|² + |β|² = {abs(alpha)**2 + abs(beta)**2}")  # 1.0
