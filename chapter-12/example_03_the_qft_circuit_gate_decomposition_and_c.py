"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.2 The QFT Circuit: Gate Decomposition and Complexity
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_03_the_qft_circuit_gate_decomposition_and_c.py
"""

from qiskit import QuantumCircuit
import numpy as np

def build_qft_circuit(n):
    """Build the QFT circuit for n qubits with explicit gate decomposition."""
    qc = QuantumCircuit(n, name=f"QFT-{n}")

    for target in range(n):
        # Hadamard on target qubit
        qc.h(target)
        # Controlled phase rotations from subsequent qubits
        for control in range(target + 1, n):
            k = control - target + 1
            angle = 2 * np.pi / (2**k)  # R_k rotation angle
            qc.cp(angle, control, target)

    # Bit-reversal permutation (swap first with last, etc.)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)

    return qc

# Build and display QFT circuits for different sizes
for n in [2, 3, 4]:
    qft = build_qft_circuit(n)
    gate_count = qft.count_ops()
    total_gates = sum(gate_count.values())

    # Count: n Hadamards + n(n-1)/2 controlled-phase + floor(n/2) swaps
    n_h = n
    n_cp = n * (n - 1) // 2
    n_swap = n // 2
    expected = n_h + n_cp + n_swap

    print(f"\n{n}-qubit QFT:")
    print(f"  Gates: {dict(gate_count)}")
    print(f"  Total: {total_gates} gates (expected: {n_h}H + {n_cp}CP + {n_swap}SWAP = {expected})")
    print(f"  Circuit depth: {qft.depth()}")

# Verify: QFT circuit produces the correct unitary
from qiskit.quantum_info import Operator

for n in [2, 3, 4]:
    N = 2**n
    omega = np.exp(2j * np.pi / N)
    QFT_expected = np.array(
        [[omega**(j*k) / np.sqrt(N) for k in range(N)] for j in range(N)]
    )
    QFT_circuit = Operator(build_qft_circuit(n)).data
    match = np.allclose(QFT_circuit, QFT_expected)
    print(f"\n{n}-qubit QFT circuit matches matrix? {match}")
