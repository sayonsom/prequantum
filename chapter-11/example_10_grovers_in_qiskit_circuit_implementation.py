"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.7 Grover's in Qiskit: Circuit Implementation
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_10_grovers_in_qiskit_circuit_implementation.py
"""

from qiskit import QuantumCircuit
from qiskit_aer.primitives import SamplerV2
import numpy as np

def run_grover_v2(n, target, shots=1024):
    """Run Grover's using SamplerV2 (Qiskit 2.x pattern)."""
    N = 2**n
    optimal_iters = int(np.round(np.pi * np.sqrt(N) / 4))

    qc = QuantumCircuit(n)
    qc.h(range(n))

    oracle = grover_oracle(n, target)
    diffuser = grover_diffusion(n)

    for _ in range(optimal_iters):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)

    qc.measure_all()

    sampler = SamplerV2()
    job = sampler.run([qc], shots=shots)
    result = job.result()
    # SamplerV2 returns BitArray; extract counts
    counts = result[0].data.meas.get_counts()
    return counts, optimal_iters

# Same interface, modern backend
for n, target in [(3, '101'), (4, '1011'), (5, '10110')]:
    counts, iters = run_grover_v2(n, target)
    top = max(counts, key=counts.get)
    print(f"n={n}: target={target}, found={top}, iters={iters}")
