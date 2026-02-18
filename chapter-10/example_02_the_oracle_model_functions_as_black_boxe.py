"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.1 The Oracle Model: Functions as Black Boxes
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_02_the_oracle_model_functions_as_black_boxe.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Build an oracle for f(x) = x₀ AND x₁ (2-bit input, 1-bit output)
# f(00)=0, f(01)=0, f(10)=0, f(11)=1

def build_oracle_and(n_input=2):
    """Oracle for f(x) = x₀ AND x₁, implemented as Toffoli gate."""
    qc = QuantumCircuit(n_input + 1, name="U_f(AND)")
    # Toffoli: flips target iff both controls are 1
    qc.ccx(0, 1, 2)  # |x₀⟩|x₁⟩|y⟩ → |x₀⟩|x₁⟩|y ⊕ (x₀ AND x₁)⟩
    return qc

# Verify: test all inputs classically
oracle = build_oracle_and()

print("Testing oracle: f(x) = x₀ AND x₁")
for x0 in [0, 1]:
    for x1 in [0, 1]:
        # Prepare |x₀ x₁ 0⟩
        qc = QuantumCircuit(3)
        if x0: qc.x(0)
        if x1: qc.x(1)
        # Apply oracle
        qc.compose(oracle, inplace=True)
        sv = Statevector.from_instruction(qc)
        # Output qubit is qubit 2
        probs = sv.probabilities([2])
        f_val = 1 if probs[1] > 0.5 else 0
        print(f"  f({x0}{x1}) = {f_val}")
