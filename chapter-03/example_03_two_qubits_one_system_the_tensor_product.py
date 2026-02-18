"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.1 Two Qubits, One System: The Tensor Product
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_03_two_qubits_one_system_the_tensor_product.py
"""

# Index 0 -> outcome "00" (both qubits are 0)
# Index 1 -> outcome "01" (qubit 0 is 0, qubit 1 is 1)
# Index 2 -> outcome "10" (qubit 0 is 1, qubit 1 is 0)
# Index 3 -> outcome "11" (both qubits are 1)

# Our state [1, 0, 0, 0] means:
print(f"P(00) = {abs(system[0])**2}")  # 1.0
print(f"P(01) = {abs(system[1])**2}")  # 0.0
print(f"P(10) = {abs(system[2])**2}")  # 0.0
print(f"P(11) = {abs(system[3])**2}")  # 0.0
# 100% chance of "00". Both qubits definitely 0. Makes sense.
