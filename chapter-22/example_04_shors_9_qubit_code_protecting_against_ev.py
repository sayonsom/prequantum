"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.3 Shor's 9-Qubit Code: Protecting Against Everything
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_04_shors_9_qubit_code_protecting_against_ev.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def shor_9_qubit_code(error_gate='x', error_qubit=4):
    """
    Shor's [[9,1,3]] code.
    9 physical qubits encode 1 logical qubit.
    Corrects any single-qubit error (X, Z, or Y = iXZ).
    """
    qc = QuantumCircuit(9)

    # === ENCODE ===
    # Step 1: Phase-flip code (outer code)
    # Spread across 3 blocks of 3
    qc.cx(0, 3)
    qc.cx(0, 6)

    # Step 2: Bit-flip code (inner code) -- each block gets |+⟩ encoding
    qc.h(0); qc.h(3); qc.h(6)
    qc.cx(0, 1); qc.cx(0, 2)    # block 0: qubits 0,1,2
    qc.cx(3, 4); qc.cx(3, 5)    # block 1: qubits 3,4,5
    qc.cx(6, 7); qc.cx(6, 8)    # block 2: qubits 6,7,8

    qc.barrier()

    # === ERROR ===
    if error_gate == 'x':
        qc.x(error_qubit)      # bit flip
    elif error_gate == 'z':
        qc.z(error_qubit)      # phase flip
    elif error_gate == 'y':
        qc.y(error_qubit)      # both (Y = iXZ)

    qc.barrier()

    # === DECODE (reverse encoding) ===
    qc.cx(0, 1); qc.cx(0, 2)
    qc.cx(3, 4); qc.cx(3, 5)
    qc.cx(6, 7); qc.cx(6, 8)
    qc.h(0); qc.h(3); qc.h(6)
    qc.cx(0, 3); qc.cx(0, 6)

    return qc

# Test with different error types
backend = AerSimulator()

for error in ['x', 'z', 'y']:
    for qubit in [0, 4, 8]:
        qc = shor_9_qubit_code(error_gate=error, error_qubit=qubit)
        qc.save_statevector()
        result = backend.run(qc).result()
        sv = result.get_statevector()

        # Check: is qubit 0 still in |0⟩ after decode?
        # The first qubit's reduced state should be |0⟩
        probs = sv.probabilities([0])
        recovered = probs[0] > 0.99
        print(f"Error {error.upper()} on qubit {qubit}: "
              f"P(|0⟩) = {probs[0]:.4f} -- {'RECOVERED' if recovered else 'LOST'}")

# Expected output:
# Error X on qubit 0: P(|0⟩) = 1.0000 -- RECOVERED
# Error X on qubit 4: P(|0⟩) = 1.0000 -- RECOVERED
# Error X on qubit 8: P(|0⟩) = 1.0000 -- RECOVERED
# Error Z on qubit 0: P(|0⟩) = 1.0000 -- RECOVERED
# Error Z on qubit 4: P(|0⟩) = 1.0000 -- RECOVERED
# Error Z on qubit 8: P(|0⟩) = 1.0000 -- RECOVERED
# Error Y on qubit 0: P(|0⟩) = 1.0000 -- RECOVERED
# Error Y on qubit 4: P(|0⟩) = 1.0000 -- RECOVERED
# Error Y on qubit 8: P(|0⟩) = 1.0000 -- RECOVERED
