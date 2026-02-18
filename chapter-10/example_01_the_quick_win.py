"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

# A 4-bit balanced oracle: f(x) = x₀ ⊕ x₂ (XOR of bits 0 and 2)
# This is balanced because exactly half of all inputs give f=1.

n = 4  # number of input bits

qc = QuantumCircuit(n + 1, n)  # n input qubits + 1 output qubit

# Step 1: Put output qubit in |−⟩ state
qc.x(n)
qc.h(n)

# Step 2: Put all input qubits in superposition
for i in range(n):
    qc.h(i)

# Step 3: Apply the oracle (f(x) = x₀ ⊕ x₂)
# For each bit that participates in f, CNOT from that qubit to output
qc.cx(0, n)  # x₀
qc.cx(2, n)  # x₂

# Step 4: Apply Hadamard to input qubits again
for i in range(n):
    qc.h(i)

# Step 5: Measure input qubits
qc.measure(range(n), range(n))

# Run
sim = AerSimulator()
result = sim.run(qc, shots=1024, seed_simulator=42).result()
counts = result.get_counts()

print(f"Measurement results: {counts}")
# If ALL input qubits measure 0 → function is CONSTANT
# If ANY input qubit measures 1 → function is BALANCED
all_zeros = '0' * n
if all_zeros in counts and counts[all_zeros] == 1024:
    print("Verdict: CONSTANT")
else:
    print("Verdict: BALANCED")
