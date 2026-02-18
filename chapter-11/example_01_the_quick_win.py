"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

n = 3  # 3 qubits → 8 possible items
target = '101'  # the item we're searching for

qc = QuantumCircuit(n, n)

# Step 1: Uniform superposition
qc.h(range(n))

# Step 2: Grover iterations (2 for N=8)
for iteration in range(2):
    # --- Oracle: flip phase of |101⟩ ---
    # |101⟩ means qubit 0 = 1, qubit 1 = 0, qubit 2 = 1
    # Flip qubits that should be 0 (qubit 1), apply multi-controlled Z, flip back
    qc.x(1)            # flip qubit 1 (the 0 in '101')
    qc.h(2)            # convert Z on qubit 2 to phase
    qc.ccx(0, 1, 2)    # Toffoli: controlled-controlled-X
    qc.h(2)            # convert back
    qc.x(1)            # unflip qubit 1

    # --- Diffusion: 2|s⟩⟨s| - I where |s⟩ = H⊗n|0⟩ ---
    qc.h(range(n))
    qc.x(range(n))
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x(range(n))
    qc.h(range(n))

# Step 3: Measure
qc.measure(range(n), range(n))

sim = AerSimulator()
result = sim.run(qc, shots=1024, seed_simulator=42).result()
counts = result.get_counts()

print(f"Searching for: {target}")
print(f"Results after 2 Grover iterations:")
for state, count in sorted(counts.items(), key=lambda x: -x[1]):
    bar = '#' * (count // 20)
    print(f"  |{state}⟩: {count:4d}/1024  {bar}")
