"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.5 The Bernstein-Vazirani Algorithm
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_07_the_bernstein_vazirani_algorithm.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def bernstein_vazirani(secret, n):
    """Find the secret string s using one query.

    secret: str, the hidden bit string (e.g., '1011')
    n: number of bits
    """
    qc = QuantumCircuit(n + 1, n)

    # Prepare: |0⟩^n|1⟩ → H → superposition + |−⟩
    qc.x(n)
    qc.h(range(n + 1))

    # Oracle: f(x) = s · x = s₀x₀ ⊕ s₁x₁ ⊕ ... ⊕ sₙ₋₁xₙ₋₁
    # For each bit sᵢ = 1, add a CNOT from qubit i to output
    for i, bit in enumerate(reversed(secret)):
        if bit == '1':
            qc.cx(i, n)

    # Apply H to input qubits
    qc.h(range(n))

    # Measure
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=1, seed_simulator=42).result()
    measured = list(result.get_counts().keys())[0]

    return measured

# Test with various secrets
print("Bernstein-Vazirani (1 query each):")
for secret in ['101', '1101', '00000', '11111', '10110011']:
    n = len(secret)
    found = bernstein_vazirani(secret, n)
    match = "OK" if found == secret else "WRONG"
    print(f"  Secret: {secret}  Found: {found}  ({match})")

print(f"\nClassical: need {len(secret)} queries (one per bit)")
print(f"Quantum: 1 query")
