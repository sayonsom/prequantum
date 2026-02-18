"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.4 Creating Entanglement: H + CNOT
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_12_creating_entanglement_h_cnot.py
"""

# The state [0.5, 0.5, 0.5, 0.5] -- is this entangled?
q0 = np.array([1, 1], dtype=complex) / np.sqrt(2)
q1 = np.array([1, 1], dtype=complex) / np.sqrt(2)
reconstructed = np.kron(q0, q1)
print(f"Reconstructed: {np.round(reconstructed, 4)}")
# [0.5, 0.5, 0.5, 0.5] -- matches!

print(f"Separable: {np.allclose(reconstructed, np.array([0.5,0.5,0.5,0.5]))}")
# True. This state is NOT entangled.
