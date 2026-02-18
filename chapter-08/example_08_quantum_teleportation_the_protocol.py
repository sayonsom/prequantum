"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.3 Quantum Teleportation: The Protocol
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_08_quantum_teleportation_the_protocol.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
import numpy as np

def teleport_and_verify(theta, phi):
    """Teleport a state parameterized by (theta, phi) and verify."""

    # Prepare the target state for reference
    prep = QuantumCircuit(1)
    prep.ry(theta, 0)
    prep.rz(phi, 0)
    target = Statevector.from_instruction(prep)

    # Build teleportation circuit: 3 qubits, 3 classical bits
    qc = QuantumCircuit(3, 3)

    # Prepare state to teleport on qubit 0
    qc.ry(theta, 0)
    qc.rz(phi, 0)

    # Create Bell pair (qubits 1, 2)
    qc.h(1)
    qc.cx(1, 2)

    # Alice's operations
    qc.cx(0, 1)
    qc.h(0)

    # Alice measures
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Bob's conditional corrections (Qiskit 2.x if_test syntax)
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(2)
    with qc.if_test((qc.clbits[0], 1)):
        qc.z(2)

    # Measure Bob's qubit
    qc.measure(2, 2)

    # Run and check Bob's qubit statistics
    sim = AerSimulator()
    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()

    # Extract Bob's qubit (clbit 2) statistics
    bob_0 = sum(v for k, v in counts.items() if k[0] == '0')  # clbit 2 (leftmost)
    bob_1 = sum(v for k, v in counts.items() if k[0] == '1')
    total = bob_0 + bob_1

    target_p0 = abs(target.data[0])**2
    target_p1 = abs(target.data[1])**2

    return target_p0, target_p1, bob_0/total, bob_1/total

# Test with several states
print("Teleportation verification:")
print(f"  {'State':20s} {'Target P(0)':>12s} {'Measured P(0)':>14s} {'Match?':>8s}")
print(f"  {'-'*60}")

for name, theta, phi in [
    ("|0⟩", 0, 0),
    ("|1⟩", np.pi, 0),
    ("|+⟩", np.pi/2, 0),
    ("Ry(1.2)Rz(0.7)|0⟩", 1.2, 0.7),
    ("Ry(2.5)Rz(1.3)|0⟩", 2.5, 1.3),
]:
    tp0, tp1, mp0, mp1 = teleport_and_verify(theta, phi)
    match = abs(tp0 - mp0) < 0.03
    print(f"  {name:20s} {tp0:12.4f} {mp0:14.4f} {'YES' if match else 'NO':>8s}")
