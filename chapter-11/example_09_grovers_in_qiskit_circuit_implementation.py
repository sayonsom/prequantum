"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.7 Grover's in Qiskit: Circuit Implementation
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_09_grovers_in_qiskit_circuit_implementation.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import numpy as np

def grover_oracle(n, target):
    """Build a phase oracle that marks |target⟩.

    target: str, e.g. '1011'
    """
    qc = QuantumCircuit(n, name=f"Oracle({target})")
    # Flip qubits where target bit is '0'
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            qc.x(i)
    # Multi-controlled Z: flip phase when all qubits are |1⟩
    # Implement as H on last qubit, multi-controlled X (MCX), H on last qubit
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    # Unflip
    for i, bit in enumerate(reversed(target)):
        if bit == '0':
            qc.x(i)
    return qc

def grover_diffusion(n):
    """Build the diffusion operator 2|s⟩⟨s| - I."""
    qc = QuantumCircuit(n, name="Diffusion")
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc

def run_grover(n, target, shots=1024):
    """Run Grover's algorithm for an n-qubit search."""
    N = 2**n
    optimal_iters = int(np.round(np.pi * np.sqrt(N) / 4))

    qc = QuantumCircuit(n, n)
    qc.h(range(n))  # uniform superposition

    oracle = grover_oracle(n, target)
    diffuser = grover_diffusion(n)

    for _ in range(optimal_iters):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)

    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=shots, seed_simulator=42).result()
    counts = result.get_counts()

    return counts, optimal_iters

# Test with increasing sizes
for n, target in [(3, '101'), (4, '1011'), (5, '10110'), (6, '101101')]:
    counts, iters = run_grover(n, target)
    N = 2**n
    top = max(counts, key=counts.get)
    top_count = counts[top]
    print(f"n={n} (N={N:3d}): target={target}, found={top} ({top_count}/1024), "
          f"iters={iters}, classical={N//2} avg queries")
