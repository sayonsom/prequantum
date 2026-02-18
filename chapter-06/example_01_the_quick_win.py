"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Build a 3-qubit GHZ circuit
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.measure([0, 1, 2], [0, 1, 2])

print(qc.draw())

# Run it
sim = AerSimulator()
result = sim.run(qc, shots=10000, seed_simulator=42).result()
counts = result.get_counts()

print("\nResults:")
for outcome in sorted(counts):
    print(f"  {outcome}: {counts[outcome]}")
