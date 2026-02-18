"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_28_break_this.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.h(0)       # BUG: extra Hadamard undoes the superposition on qubit 0
qc.measure([0, 1, 2], [0, 1, 2])

sim = AerSimulator()
result = sim.run(qc, shots=10000, seed_simulator=42).result()
counts = result.get_counts()

print("Results:")
for outcome in sorted(counts):
    print(f"  {outcome}: {counts[outcome]}")
# This gives more than just 000 and 111!
