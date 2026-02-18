"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.3 The Deutsch-Jozsa Algorithm
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_04_the_deutsch_jozsa_algorithm.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import numpy as np

def deutsch_jozsa(oracle, n):
    """Run the Deutsch-Jozsa algorithm.

    oracle: QuantumCircuit acting on n+1 qubits (n input + 1 output)
    n: number of input bits
    Returns: 'constant' or 'balanced'
    """
    qc = QuantumCircuit(n + 1, n)

    # Step 1-2: Prepare |0⟩^n|1⟩, then apply H to all
    qc.x(n)              # output qubit → |1⟩
    qc.h(range(n + 1))   # all qubits → superposition

    # Step 3: Apply oracle
    qc.compose(oracle, inplace=True)

    # Step 4: H on input qubits
    qc.h(range(n))

    # Step 5: Measure input qubits
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=1, seed_simulator=42).result()
    measured = list(result.get_counts().keys())[0]

    return 'constant' if measured == '0' * n else 'balanced'

# --- Test with different oracles ---

# Constant oracle: f(x) = 0 for all x (do nothing)
def make_constant_0(n):
    return QuantumCircuit(n + 1, name="f=0")

# Constant oracle: f(x) = 1 for all x (flip output)
def make_constant_1(n):
    qc = QuantumCircuit(n + 1, name="f=1")
    qc.x(n)  # Always flip the output qubit
    return qc

# Balanced oracle: f(x) = x₀ (parity of first bit)
def make_balanced_x0(n):
    qc = QuantumCircuit(n + 1, name="f=x0")
    qc.cx(0, n)
    return qc

# Balanced oracle: f(x) = x₀ ⊕ x₁ ⊕ x₂ (parity of first 3 bits)
def make_balanced_parity(n):
    qc = QuantumCircuit(n + 1, name="f=x0⊕x1⊕x2")
    for i in range(min(3, n)):
        qc.cx(i, n)
    return qc

n = 5  # 5-bit input → 2⁵ = 32 possible inputs
print(f"Deutsch-Jozsa on {n}-bit functions (1 query each):")
print(f"  f=0 (constant):       {deutsch_jozsa(make_constant_0(n), n)}")
print(f"  f=1 (constant):       {deutsch_jozsa(make_constant_1(n), n)}")
print(f"  f=x₀ (balanced):      {deutsch_jozsa(make_balanced_x0(n), n)}")
print(f"  f=x₀⊕x₁⊕x₂ (balanced): {deutsch_jozsa(make_balanced_parity(n), n)}")
print(f"\nClassical worst case: {2**(n-1) + 1} queries")
print(f"Quantum: 1 query")
