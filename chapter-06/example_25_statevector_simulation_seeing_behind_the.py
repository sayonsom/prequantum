"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.9 Statevector Simulation: Seeing Behind the Curtain
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_25_statevector_simulation_seeing_behind_the.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
import numpy as np

# Using Statevector to verify gate identities from Chapter 5
qc1 = QuantumCircuit(1)
qc1.h(0)
qc1.z(0)
qc1.h(0)

qc2 = QuantumCircuit(1)
qc2.x(0)

sv1 = Statevector.from_instruction(qc1)
sv2 = Statevector.from_instruction(qc2)

# Apply both to |0⟩
ket_0 = Statevector.from_label('0')
result1 = ket_0.evolve(qc1)
result2 = ket_0.evolve(qc2)

print(f"HZH|0⟩ = {np.round(result1.data, 4)}")
print(f"X|0⟩   = {np.round(result2.data, 4)}")
print(f"HZH = X confirmed: {np.allclose(result1.data, result2.data)}")  # True

# You can also extract the full unitary matrix of a circuit
op = Operator(qc1)
print(f"\nUnitary of HZH:\n{np.round(op.data, 4)}")
# Should match the X gate matrix (up to global phase)
