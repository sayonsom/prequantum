"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.4 Eigenvalues and Phase Estimation
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_06_eigenvalues_and_phase_estimation.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def qpe(unitary_gate, eigenvector_prep, n_count, n_target):
    """Quantum Phase Estimation.

    unitary_gate: function(qc, power, ctrl, targets) that applies controlled-U^power
    eigenvector_prep: function(qc, targets) that prepares |u⟩
    n_count: number of counting qubits (precision)
    n_target: number of target qubits
    """
    qc = QuantumCircuit(n_count + n_target, n_count)

    # Step 1: Superposition on counting register
    qc.h(range(n_count))

    # Prepare eigenvector on target register
    eigenvector_prep(qc, list(range(n_count, n_count + n_target)))

    # Step 2: Controlled-U^(2^j)
    for j in range(n_count):
        power = 2**j
        unitary_gate(qc, power, j, list(range(n_count, n_count + n_target)))

    # Step 3: Inverse QFT on counting register
    for i in range(n_count // 2):
        qc.swap(i, n_count - 1 - i)
    for i in range(n_count):
        for j in range(i):
            qc.cp(-np.pi / 2**(i - j), j, i)
        qc.h(i)

    # Step 4: Measure
    qc.measure(range(n_count), range(n_count))
    return qc

# --- Test: estimate phase of the T gate ---
# T|1⟩ = e^(iπ/4)|1⟩ → φ = 1/8

def t_gate_controlled(qc, power, ctrl, targets):
    """Apply controlled-T^power."""
    angle = np.pi / 4 * power
    qc.cp(angle, ctrl, targets[0])

def prep_ket_1(qc, targets):
    """Prepare |1⟩."""
    qc.x(targets[0])

qc = qpe(t_gate_controlled, prep_ket_1, n_count=3, n_target=1)

sim = AerSimulator()
result = sim.run(qc, shots=1024, seed_simulator=42).result()
counts = result.get_counts()

print("QPE for T gate (expected phase φ = 1/8 = 0.125):")
for state, count in sorted(counts.items(), key=lambda x: -x[1]):
    measured_phase = int(state, 2) / 2**3
    print(f"  |{state}⟩ ({count:4d}/1024)  →  φ = {measured_phase:.4f}")
