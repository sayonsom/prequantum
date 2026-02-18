"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.4 From Your Qubit to Qiskit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_12_from_your_qubit_to_qiskit.py
"""

# pip install qiskit qiskit-aer
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)
qc.h(0)         # Apply Hadamard to qubit 0 (same as our q.hadamard())
qc.measure(0, 0) # Measure qubit 0, store in classical bit 0

print(qc.draw())
#      ┌───┐┌─┐
# q_0: ┤ H ├┤M├
#      └───┘└╥┘
# c: 1/══════╩═
#             0

# Run on a simulator -- same as our measurement loop
sim = AerSimulator()
result = sim.run(qc, shots=10000, seed_simulator=42).result()
counts = result.get_counts()
print(counts)  # {'0': ~5000, '1': ~5000}
