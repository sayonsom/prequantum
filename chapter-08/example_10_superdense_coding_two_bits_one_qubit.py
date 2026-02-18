"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.4 Superdense Coding: Two Bits, One Qubit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_10_superdense_coding_two_bits_one_qubit.py
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# After Alice's encoding, the shared state is one of the four Bell states.
# Bob's decoding maps each Bell state to a unique computational basis state.

encodings = {
    '00': 'I',
    '01': 'X',
    '10': 'Z',
    '11': 'ZX',
}

print("Superdense coding: intermediate states")
print(f"{'Msg':>4s} {'Gate':>4s} {'Bell state after encoding':>40s} {'Decoded':>10s}")

for msg, gate_name in encodings.items():
    qc = QuantumCircuit(2)
    # Create Bell pair
    qc.h(0)
    qc.cx(0, 1)
    # Alice encodes
    if msg == '01':
        qc.x(0)
    elif msg == '10':
        qc.z(0)
    elif msg == '11':
        qc.z(0)
        qc.x(0)

    # State after encoding (before Bob decodes)
    sv_encoded = Statevector.from_instruction(qc)

    # Bob decodes
    qc.cx(0, 1)
    qc.h(0)
    sv_decoded = Statevector.from_instruction(qc)

    print(f"  {msg:>3s} {gate_name:>4s}  "
          f"{str(np.round(sv_encoded.data, 3)):>40s}  "
          f"{str(np.round(sv_decoded.data, 3)):>10s}")

# Verify orthogonality of the four Bell states
print("\nBell state orthogonality (all cross-overlaps should be 0):")
bell_states = []
for msg in ['00', '01', '10', '11']:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    if msg == '01': qc.x(0)
    elif msg == '10': qc.z(0)
    elif msg == '11': qc.z(0); qc.x(0)
    bell_states.append(Statevector.from_instruction(qc))

names = ['Φ+', 'Ψ+', 'Φ-', 'Ψ-']
for i in range(4):
    for j in range(4):
        overlap = abs(bell_states[i].inner(bell_states[j]))**2
        if i != j and overlap > 1e-10:
            print(f"  ⟨{names[i]}|{names[j]}⟩ = {overlap:.4f} ← NOT ZERO!")
    row = [f"{abs(bell_states[i].inner(bell_states[j]))**2:.1f}" for j in range(4)]
    print(f"  |{names[i]}⟩: [{', '.join(row)}]")
