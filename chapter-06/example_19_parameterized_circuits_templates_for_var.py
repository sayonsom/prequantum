"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.7 Parameterized Circuits: Templates for Variational Algorithms
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_19_parameterized_circuits_templates_for_var.py
"""

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterVector
from qiskit.quantum_info import Statevector
import numpy as np

# Single parameter
theta = Parameter('θ')

qc = QuantumCircuit(1)
qc.ry(theta, 0)

print(qc.draw())
# The circuit is a *template* -- not yet runnable

# Bind a specific value
bound = qc.assign_parameters({theta: np.pi/4})
sv = Statevector.from_instruction(bound)
print(f"\nθ=π/4: P(0) = {abs(sv.data[0])**2:.4f}, "
      f"P(1) = {abs(sv.data[1])**2:.4f}")

# Bind multiple values to see the parameter sweep
for angle in [0, np.pi/4, np.pi/2, np.pi]:
    bound = qc.assign_parameters({theta: angle})
    sv = Statevector.from_instruction(bound)
    print(f"  θ={angle/np.pi:.2f}π: "
          f"|0⟩ amp={sv.data[0]:.4f}, |1⟩ amp={sv.data[1]:.4f}")
