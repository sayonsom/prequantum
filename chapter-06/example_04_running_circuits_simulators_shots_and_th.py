"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.2 Running Circuits: Simulators, Shots, and the Primitives API
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_04_running_circuits_simulators_shots_and_th.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Build a simple circuit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

sim = AerSimulator()

# Run with different shot counts
for shots in [10, 100, 1000, 10000]:
    result = sim.run(qc, shots=shots, seed_simulator=42).result()
    counts = result.get_counts()
    zeros = counts.get('0', 0)
    ones = counts.get('1', 0)
    print(f"  {shots:5d} shots: 0→{zeros:5d} ({zeros/shots*100:5.1f}%)  "
          f"1→{ones:5d} ({ones/shots*100:5.1f}%)")
