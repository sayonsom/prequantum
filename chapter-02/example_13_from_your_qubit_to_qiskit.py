"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.4 From Your Qubit to Qiskit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_13_from_your_qubit_to_qiskit.py
"""

qc2 = QuantumCircuit(1, 1)
qc2.h(0)         # First Hadamard: creates superposition
qc2.h(0)         # Second Hadamard: interference brings us back
qc2.measure(0, 0)

result2 = sim.run(qc2, shots=10000, seed_simulator=42).result()
counts2 = result2.get_counts()
print(counts2)  # {'0': 10000} -- always 0, just like our numpy version
