"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_14_break_this.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def buggy_superdense(message):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)

    if message == '00':
        pass
    elif message == '01':
        qc.x(0)
    elif message == '10':
        qc.z(0)
    elif message == '11':
        qc.x(0)      # BUG: should be Z then X (order matters!)
        qc.z(0)

    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
    return qc

sim = AerSimulator()
for msg in ['00', '01', '10', '11']:
    qc = buggy_superdense(msg)
    result = sim.run(qc, shots=1000, seed_simulator=42).result()
    counts = result.get_counts()
    decoded = max(counts, key=counts.get)
    status = "OK" if decoded == msg else "WRONG!"
    print(f"  Sent: {msg}  Decoded: {decoded}  {status}")
