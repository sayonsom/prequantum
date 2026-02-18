"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.7 Parameterized Circuits: Templates for Variational Algorithms
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_20_parameterized_circuits_templates_for_var.py
"""

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
import numpy as np

# ParameterVector for circuits with many parameters
params = ParameterVector('θ', 6)

# A simple variational ansatz: alternating Ry layers and CX entanglement
qc = QuantumCircuit(3)

# Layer 1: Ry rotations
for i in range(3):
    qc.ry(params[i], i)

# Entangling layer
qc.cx(0, 1)
qc.cx(1, 2)

# Layer 2: Ry rotations
for i in range(3):
    qc.ry(params[i + 3], i)

print(qc.draw())
print(f"\nNumber of parameters: {qc.num_parameters}")
print(f"Parameters: {[p.name for p in qc.parameters]}")

# Bind random values
rng = np.random.default_rng(42)
values = rng.uniform(0, 2 * np.pi, 6)
bound = qc.assign_parameters(dict(zip(params, values)))
print(f"\nBound circuit depth: {bound.depth()}")
