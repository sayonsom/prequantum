"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.3 Multi-Qubit Circuits and the Gate Library
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_09_multi_qubit_circuits_and_the_gate_librar.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# === Phase gates in Qiskit ===
sim = AerSimulator()

# The H-phase-H sandwich from Chapter 5
for gate_name, gate_fn in [("T", "t"), ("S", "s"), ("Z", "z")]:
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    getattr(qc, gate_fn)(0)  # Apply T, S, or Z
    qc.h(0)
    qc.measure(0, 0)
    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()
    zeros = counts.get('0', 0)
    ones = counts.get('1', 0)
    print(f"  H·{gate_name}·H|0⟩: 0→{zeros/100:.1f}%  1→{ones/100:.1f}%")
# H·T·H|0⟩: 0→85.4%  1→14.6%   (biased)
# H·S·H|0⟩: 0→50.0%  1→50.0%   (equal but different state)
# H·Z·H|0⟩: 0→0.0%   1→100.0%  (certainty! HZH = X)
