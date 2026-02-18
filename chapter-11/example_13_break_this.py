"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_13_break_this.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def buggy_grover(n, target):
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    N = 2**n
    iters = int(np.round(np.pi * np.sqrt(N) / 4))

    for _ in range(iters):
        # Oracle
        for i, bit in enumerate(reversed(target)):
            if bit == '0':
                qc.x(i)
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        # BUG: missing the un-flip of X gates!
        # Should have another loop here to undo the X gates on '0' qubits

        # Diffusion
        qc.h(range(n))
        qc.x(range(n))
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
        qc.x(range(n))
        qc.h(range(n))

    qc.measure(range(n), range(n))
    sim = AerSimulator()
    result = sim.run(qc, shots=1024, seed_simulator=42).result()
    counts = result.get_counts()
    return max(counts, key=counts.get)

# Test
for target in ['111', '101', '001']:
    found = buggy_grover(3, target)
    status = "OK" if found == target else "WRONG"
    print(f"Target: {target}  Found: {found}  {status}")
