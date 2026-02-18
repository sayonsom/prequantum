"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.4 Creating Entanglement: H + CNOT
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_09_creating_entanglement_h_cnot.py
"""

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

state = np.array([1, 0, 0, 0], dtype=complex)  # |00>

# Hadamard on qubit 0
H_on_q0 = np.kron(H, I)
state = H_on_q0 @ state
print(f"After H on q0: {np.round(state, 4)}")
# [0.7071, 0, 0.7071, 0]
