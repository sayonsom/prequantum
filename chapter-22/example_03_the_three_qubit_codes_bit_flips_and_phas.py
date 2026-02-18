"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.2 The Three-Qubit Codes: Bit Flips and Phase Flips
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_03_the_three_qubit_codes_bit_flips_and_phas.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def run_code(error_type='bit_flip', error_qubit=1):
    """Run 3-qubit error correction for bit-flip or phase-flip."""
    qc = QuantumCircuit(5, 3)  # 3 data + 2 ancilla, 3 classical

    # Prepare |+⟩ state on qubit 0 (to see phase effects)
    qc.h(0)

    if error_type == 'phase_flip':
        # PHASE-FLIP CODE: encode in Hadamard basis
        # |+⟩ → |+++⟩, |−⟩ → |−−−⟩
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.h(0); qc.h(1); qc.h(2)  # switch to Hadamard basis

        # Phase flip error (Z gate)
        qc.z(error_qubit)
        qc.barrier()

        # Detect in Hadamard basis
        qc.h(0); qc.h(1); qc.h(2)  # back to computational basis
        qc.cx(0, 3); qc.cx(1, 3)   # parity checks
        qc.cx(1, 4); qc.cx(2, 4)
        qc.h(0); qc.h(1); qc.h(2)  # return to Hadamard basis

    else:
        # BIT-FLIP CODE: encode in computational basis
        # |0⟩ → |000⟩, |1⟩ → |111⟩
        qc.cx(0, 1)
        qc.cx(0, 2)

        # Bit flip error (X gate)
        qc.x(error_qubit)
        qc.barrier()

        # Detect parity
        qc.cx(0, 3); qc.cx(1, 3)
        qc.cx(1, 4); qc.cx(2, 4)

    # Measure syndrome
    qc.measure(3, 0)
    qc.measure(4, 1)

    # Correction based on syndrome
    qc.x(1).c_if(qc.clbits[0:2], 3)  # syndrome 11 → qubit 1
    qc.x(0).c_if(qc.clbits[0:2], 2)  # syndrome 10 → qubit 0
    qc.x(2).c_if(qc.clbits[0:2], 1)  # syndrome 01 → qubit 2

    # Decode
    if error_type == 'phase_flip':
        qc.h(0); qc.h(1); qc.h(2)
    qc.cx(0, 2)
    qc.cx(0, 1)

    # Measure original qubit (should be |+⟩)
    qc.h(0)  # convert |+⟩ to |0⟩ for measurement
    qc.measure(0, 2)

    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    return result.get_counts()

# Test both codes
print("Bit-flip error on qubit 1:")
counts = run_code('bit_flip', 1)
print(f"  {counts}")
print(f"  Qubit recovered: {'0' in str(max(counts, key=counts.get))}")

print("\nPhase-flip error on qubit 1:")
counts = run_code('phase_flip', 1)
print(f"  {counts}")
print(f"  Qubit recovered: {'0' in str(max(counts, key=counts.get))}")

# Expected output:
# Bit-flip error on qubit 1:
#   {'0 11': 1024}
#   Qubit recovered: True
#
# Phase-flip error on qubit 1:
#   {'0 11': 1024}
#   Qubit recovered: True
