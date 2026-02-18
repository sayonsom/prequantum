"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# The state we want to teleport: an arbitrary qubit
theta = 1.2  # some angle
phi = 0.7    # some other angle

# Alice has the state to teleport (qubit 0)
# Alice and Bob share a Bell pair (qubits 1, 2)
qc = QuantumCircuit(3, 2)

# Prepare the mystery state on qubit 0
qc.ry(theta, 0)
qc.rz(phi, 0)

# Record what the state should be
prep = QuantumCircuit(1)
prep.ry(theta, 0)
prep.rz(phi, 0)
original_state = Statevector.from_instruction(prep)
print(f"Original state to teleport: {np.round(original_state.data, 4)}")

# Create Bell pair between qubits 1 and 2 (shared by Alice and Bob)
qc.h(1)
qc.cx(1, 2)

# === Teleportation protocol ===
# Alice entangles her qubit with her half of the Bell pair
qc.cx(0, 1)
qc.h(0)

# Alice measures her two qubits
qc.measure(0, 0)
qc.measure(1, 1)

# Bob applies corrections based on Alice's measurement results
# Uses Qiskit's if_test context manager (standard since Qiskit 1.0+)
# Note: the older c_if() syntax is removed in Qiskit 2.x
with qc.if_test((qc.clbits[1], 1)):
    qc.x(2)   # If Alice's qubit 1 = 1, apply X
with qc.if_test((qc.clbits[0], 1)):
    qc.z(2)   # If Alice's qubit 0 = 1, apply Z

print(f"\nTeleportation circuit:")
print(qc.draw())
