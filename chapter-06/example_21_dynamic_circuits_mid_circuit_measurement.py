"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.8 Dynamic Circuits: Mid-Circuit Measurement and Classical Feedforward
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_21_dynamic_circuits_mid_circuit_measurement.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Quantum teleportation -- the canonical dynamic circuit
# Alice wants to teleport the state of qubit 0 to Bob's qubit 2

qc = QuantumCircuit(3, 2)

# Step 1: Prepare a state to teleport (on qubit 0)
qc.ry(1.2, 0)  # Some arbitrary state (not |0⟩ or |1⟩)

# Step 2: Create a Bell pair between qubits 1 and 2
qc.h(1)
qc.cx(1, 2)

qc.barrier()  # Visual separator

# Step 3: Alice's operations (Bell measurement on qubits 0,1)
qc.cx(0, 1)
qc.h(0)

# Step 4: Mid-circuit measurement (this is the "dynamic" part)
qc.measure(0, 0)
qc.measure(1, 1)

qc.barrier()

# Step 5: Classical feedforward -- Bob's corrections
# If Alice measured 1 on qubit 1, apply X to qubit 2
with qc.if_test((1, 1)):  # classical bit 1 == 1
    qc.x(2)

# If Alice measured 1 on qubit 0, apply Z to qubit 2
with qc.if_test((0, 1)):  # classical bit 0 == 1
    qc.z(2)

print(qc.draw())
