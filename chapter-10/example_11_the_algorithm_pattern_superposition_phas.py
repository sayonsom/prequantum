"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.8 The Algorithm Pattern: Superposition → Phase → Interfere → Measure
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_11_the_algorithm_pattern_superposition_phas.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def oracle_algorithm_template(oracle, n, name="Algorithm"):
    """The shared template behind DJ, BV, and related algorithms."""
    qc = QuantumCircuit(n + 1, n)

    # Step 1-2: Superposition + phase kickback setup
    qc.x(n)               # output → |1⟩
    qc.h(range(n + 1))    # inputs → superposition, output → |−⟩

    # Step 3: Oracle (the only part that changes between algorithms)
    qc.compose(oracle, inplace=True)

    # Step 4: Interference (H^⊗n on inputs)
    qc.h(range(n))

    # Step 5: Measure
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=1024, seed_simulator=42).result()
    return result.get_counts()

# Same template, different oracles, different answers
n = 4

# DJ: constant oracle → measures 0000
constant_oracle = QuantumCircuit(n + 1, name="f=0")
print("Constant oracle:", oracle_algorithm_template(constant_oracle, n))

# DJ: balanced oracle → measures non-zero
balanced_oracle = QuantumCircuit(n + 1, name="f=x0⊕x1")
balanced_oracle.cx(0, n)
balanced_oracle.cx(1, n)
print("Balanced oracle:", oracle_algorithm_template(balanced_oracle, n))

# BV: hidden string "1010" → measures 1010
bv_oracle = QuantumCircuit(n + 1, name="f=s·x")
bv_oracle.cx(1, n)  # s₁=1
bv_oracle.cx(3, n)  # s₃=1
print("BV oracle (s=1010):", oracle_algorithm_template(bv_oracle, n))
