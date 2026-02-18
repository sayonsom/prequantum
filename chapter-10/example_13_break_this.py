"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_13_break_this.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def buggy_bv(secret, n):
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(range(n + 1))

    # Oracle for f(x) = s · x
    for i, bit in enumerate(secret):  # BUG: should be enumerate(reversed(secret))
        if bit == '1':
            qc.cx(i, n)

    qc.h(range(n))
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=1, seed_simulator=42).result()
    measured = list(result.get_counts().keys())[0]
    return measured[::-1]

# Test
for secret in ['101', '110', '010']:
    found = buggy_bv(secret, len(secret))
    status = "OK" if found == secret else "WRONG"
    print(f"Secret: {secret}  Found: {found}  {status}")
