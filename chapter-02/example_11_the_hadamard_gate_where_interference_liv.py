"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.3 The Hadamard Gate: Where Interference Lives
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_11_the_hadamard_gate_where_interference_liv.py
"""

# H applied twice to "definitely 0"
q = Qubit()               # state = [1, 0]
q.hadamard()               # state = [0.7071, 0.7071]
q.hadamard()               # state = [?, ?]
print(f"After H twice: {q}")  # Qubit(state=[1.+0.j, 0.+0.j])  -- back to start!

# Verify: H times H is the identity matrix
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
HH = H @ H
print(np.round(HH, 4))
# [[1. 0.]
#  [0. 1.]]
