"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.2 Running Circuits: Simulators, Shots, and the Primitives API
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_07_running_circuits_simulators_shots_and_th.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# A circuit with a biased outcome (not 50/50)
qc = QuantumCircuit(1, 1)
qc.ry(0.8, 0)  # Ry rotation: creates unequal superposition
qc.measure(0, 0)

sim = AerSimulator()
result = sim.run(qc, shots=10000, seed_simulator=42).result()
counts = result.get_counts()
print(f"Biased circuit: {counts}")
# Roughly 85% zeros, 15% ones (depends on the Ry angle)

# Access the statevector (before measurement) for verification
from qiskit.quantum_info import Statevector

qc_no_measure = QuantumCircuit(1)
qc_no_measure.ry(0.8, 0)
sv = Statevector.from_instruction(qc_no_measure)
print(f"\nStatevector: {sv.data}")
print(f"P(0) = {abs(sv.data[0])**2:.4f}")
print(f"P(1) = {abs(sv.data[1])**2:.4f}")
