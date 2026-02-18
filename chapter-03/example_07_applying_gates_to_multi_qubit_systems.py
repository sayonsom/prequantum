"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.2 Applying Gates to Multi-Qubit Systems
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_07_applying_gates_to_multi_qubit_systems.py
"""

state = np.array([1, 0, 0, 0], dtype=complex)  # both qubits = 0
after_H = H_on_q0 @ state

for i, label in enumerate(["00", "01", "10", "11"]):
    print(f"  P({label}) = {abs(after_H[i])**2:.4f}")
# P(00) = 0.5000
# P(01) = 0.0000
# P(10) = 0.5000
# P(11) = 0.0000
