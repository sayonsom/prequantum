"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.4 Superdense Coding: Two Bits, One Qubit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_09_superdense_coding_two_bits_one_qubit.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def superdense_coding(message):
    """Send a 2-bit message using superdense coding.

    message: str, one of '00', '01', '10', '11'
    """
    qc = QuantumCircuit(2, 2)

    # Step 1: Create shared Bell pair
    qc.h(0)
    qc.cx(0, 1)
    # Alice gets qubit 0, Bob gets qubit 1

    # Step 2: Alice encodes her 2-bit message on her single qubit
    if message == '00':
        pass          # I: do nothing → encodes 00
    elif message == '01':
        qc.x(0)      # X: bit flip → encodes 01
    elif message == '10':
        qc.z(0)      # Z: phase flip → encodes 10
    elif message == '11':
        qc.z(0)      # ZX: both → encodes 11
        qc.x(0)

    # Step 3: Alice sends her qubit to Bob (physical transfer)

    # Step 4: Bob decodes -- reverse the Bell creation
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    return qc

# Test all four messages
sim = AerSimulator()
print("Superdense coding:")
for msg in ['00', '01', '10', '11']:
    qc = superdense_coding(msg)
    result = sim.run(qc, shots=1000, seed_simulator=42).result()
    counts = result.get_counts()
    decoded = max(counts, key=counts.get)
    print(f"  Sent: {msg}  →  Decoded: {decoded}  "
          f"(counts: {dict(sorted(counts.items()))})")
