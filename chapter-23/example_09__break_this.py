"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 4: The AI Lab > 🐛 Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_09__break_this.py
"""

import time
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# "Quantum advantage demonstrated!"
n_assets = 4
np.random.seed(42)

# Classical: brute force
t0 = time.time()
returns = np.random.randn(n_assets)
best = None
for bits in range(2 ** n_assets):
    portfolio = [(bits >> i) & 1 for i in range(n_assets)]
    ret = sum(r * w for r, w in zip(returns, portfolio))
    if best is None or ret > best:
        best = ret
t_classical = time.time() - t0

# Quantum: QAOA
t0 = time.time()
qc = QuantumCircuit(n_assets)
qc.h(range(n_assets))
qc.measure_all()
backend = AerSimulator()
result = backend.run(qc, shots=1000).result()
counts = result.get_counts()
best_quantum = max(counts, key=counts.get)
t_quantum = time.time() - t0

print(f"Classical: {t_classical:.4f}s")
print(f"Quantum:   {t_quantum:.4f}s")
print(f"Speedup:   {t_classical/t_quantum:.1f}x")
print("Quantum advantage achieved!")
