"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.8 Dynamic Circuits: Mid-Circuit Measurement and Classical Feedforward
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_22_dynamic_circuits_mid_circuit_measurement.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Repeat-until-success: prepare |1⟩ using only H and measurement
# (silly example, but demonstrates the pattern)
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# If we measured 0, try again (apply H and measure again)
with qc.if_test((0, 0)):  # if classical bit 0 == 0
    qc.h(0)
    qc.measure(0, 0)

sim = AerSimulator()
result = sim.run(qc, shots=10000, seed_simulator=42).result()
counts = result.get_counts()
print(f"Results: {counts}")
# Much higher probability of getting 1 than a single H+measure
