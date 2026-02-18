"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.8 Dynamic Circuits: Mid-Circuit Measurement and Classical Feedforward
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_23_dynamic_circuits_mid_circuit_measurement.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# GHZ state using dynamic circuits (constant depth!)
# Traditional GHZ needs O(n) depth for n qubits
# Dynamic circuits can do it in O(1) depth using measurement + feedforward

n = 4
qc = QuantumCircuit(n, n - 1)

# Put all qubits in superposition simultaneously (depth 1)
for i in range(n):
    qc.h(i)

# Measure all but the first qubit (depth 2)
for i in range(1, n):
    qc.measure(i, i - 1)

# Classically-controlled corrections (depth 3, regardless of n)
for i in range(1, n):
    with qc.if_test((i - 1, 1)):  # if qubit i measured 1
        qc.z(0)  # apply phase correction

# This creates a GHZ-like entangled state in constant depth
# The traditional approach needs depth O(n)
print(qc.draw())
print(f"Circuit depth: {qc.depth()}")
