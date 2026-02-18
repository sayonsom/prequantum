"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_12_break_this.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

# QPE for S gate: S|1⟩ = i|1⟩ = e^(2πi·0.25)|1⟩
# Expected phase: 0.25

n_count = 3
qc = QuantumCircuit(n_count + 1, n_count)

qc.h(range(n_count))
qc.x(n_count)  # prepare |1⟩

# Controlled-S^(2^j)
for j in range(n_count):
    angle = np.pi / 2 * (2**j)  # S = diag(1, i) = phase π/2
    qc.cp(angle, j, n_count)

# Inverse QFT (BUG: missing qubit swap for bit reversal!)
for i in range(n_count):
    for j in range(i):
        qc.cp(-np.pi / 2**(i - j), j, i)
    qc.h(i)

qc.measure(range(n_count), range(n_count))

sim = AerSimulator()
result = sim.run(qc, shots=1024, seed_simulator=42).result()
counts = result.get_counts()

print("QPE for S gate (expected φ = 0.25):")
for state, count in sorted(counts.items(), key=lambda x: -x[1]):
    phase = int(state, 2) / 2**n_count
    print(f"  |{state}⟩ ({count:4d}/1024)  →  φ = {phase:.4f}")
