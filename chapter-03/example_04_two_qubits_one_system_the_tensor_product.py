"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.1 Two Qubits, One System: The Tensor Product
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_04_two_qubits_one_system_the_tensor_product.py
"""

# kron([a, b], [c, d]) = [a*c, a*d, b*c, b*d]
q0 = np.array([0.6, 0.8], dtype=complex)
q1 = np.array([0.5, 0.866], dtype=complex)

system = np.kron(q0, q1)
print(f"np.kron result: {np.round(system, 4)}")
# [0.3, 0.5196, 0.4, 0.6928]

# Manual computation
manual = np.array([
    q0[0] * q1[0],  # a*c -> amplitude for "00"
    q0[0] * q1[1],  # a*d -> amplitude for "01"
    q0[1] * q1[0],  # b*c -> amplitude for "10"
    q0[1] * q1[1],  # b*d -> amplitude for "11"
])
print(f"Manual result:  {np.round(manual, 4)}")
print(f"Match: {np.allclose(system, manual)}")  # True
