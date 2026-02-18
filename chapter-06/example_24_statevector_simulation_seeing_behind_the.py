"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.9 Statevector Simulation: Seeing Behind the Curtain
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_24_statevector_simulation_seeing_behind_the.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Bell state circuit (no measurement)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Get the exact statevector
sv = Statevector.from_instruction(qc)
print(f"Statevector: {np.round(sv.data, 4)}")
# [0.7071+0.j 0.+0.j 0.+0.j 0.7071+0.j]

# Compare to our numpy version from Chapter 3
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
state = np.array([1, 0, 0, 0], dtype=complex)
state = np.kron(H, I) @ state
state = CNOT @ state

print(f"Numpy result: {np.round(state, 4)}")
print(f"Match: {np.allclose(sv.data, state)}")  # True

# Probabilities from the statevector
probs = sv.probabilities()
print(f"\nProbabilities: {np.round(probs, 4)}")
# [0.5 0.  0.  0.5]

# You can also get probabilities as a dictionary
probs_dict = sv.probabilities_dict()
print(f"As dictionary: {probs_dict}")
# {'00': 0.5, '11': 0.5}
