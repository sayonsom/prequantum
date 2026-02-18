"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.3 The Hadamard Gate: Where Interference Lives
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_10_the_hadamard_gate_where_interference_liv.py
"""

q1 = Qubit([0, 1])
print(f"Before H: {q1}")  # Qubit(state=[0.+0.j, 1.+0.j])

q1.hadamard()
print(f"After H:  {q1}")  # Qubit(state=[0.7071+0.j, -0.7071+0.j])
