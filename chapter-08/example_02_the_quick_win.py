"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_02_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

theta = 1.2
phi = 0.7

# What the teleported state should be
prep = QuantumCircuit(1)
prep.ry(theta, 0)
prep.rz(phi, 0)
target_state = Statevector.from_instruction(prep)
print(f"Target state: {np.round(target_state.data, 4)}")

# Simulate teleportation for each possible measurement outcome
for m0, m1 in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    qc = QuantumCircuit(3)

    # Prepare state to teleport
    qc.ry(theta, 0)
    qc.rz(phi, 0)

    # Create Bell pair (qubits 1, 2)
    qc.h(1)
    qc.cx(1, 2)

    # Alice's part: entangle and "measure" (we simulate by projecting)
    qc.cx(0, 1)
    qc.h(0)

    # Instead of measuring, we simulate a specific outcome
    # by applying the correction Bob would make
    if m1 == 1:
        qc.x(2)
    if m0 == 1:
        qc.z(2)

    # Get the full 3-qubit statevector
    sv = Statevector.from_instruction(qc)

    # Extract Bob's qubit state (qubit 2)
    # After Alice's measurement, Bob's qubit should match the target
    # We check by computing overlap
    probs = sv.probabilities([2])  # marginal on qubit 2
    print(f"  m0={m0}, m1={m1}: Bob's qubit probs = {np.round(probs, 4)}  "
          f"(target: {np.round(np.abs(target_state.data)**2, 4)})")
