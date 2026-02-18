"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.1 Two Qubits, One System: The Tensor Product
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_02_two_qubits_one_system_the_tensor_product.py
"""

import numpy as np

q0 = np.array([1, 0], dtype=complex)  # Qubit 0: definitely 0
q1 = np.array([1, 0], dtype=complex)  # Qubit 1: definitely 0

system = np.kron(q0, q1)
print(f"System state: {system}")
# System state: [1.+0.j 0.+0.j 0.+0.j 0.+0.j]

print(f"Number of amplitudes: {len(system)}")
# Number of amplitudes: 4
