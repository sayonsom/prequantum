"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.1 What Goes Wrong: A Taxonomy of Quantum Errors
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_02_what_goes_wrong_a_taxonomy_of_quantum_er.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

# Build three noise models, each with one type of error

def run_noisy(circuit, noise_model, shots=10000):
    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(circuit, shots=shots, seed_simulator=42).result()
    return result.get_counts()

# Circuit: prepare |+⟩, then measure (should be ~50/50)
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# 1. Bit-flip noise (X error) on Hadamard
nm_bitflip = NoiseModel()
nm_bitflip.add_all_qubit_quantum_error(
    pauli_error([('X', 0.1), ('I', 0.9)]), ['h'])

# 2. Phase-flip noise (Z error) on Hadamard
nm_phaseflip = NoiseModel()
nm_phaseflip.add_all_qubit_quantum_error(
    pauli_error([('Z', 0.1), ('I', 0.9)]), ['h'])

# 3. Depolarizing noise (X, Y, or Z each with equal probability)
nm_depol = NoiseModel()
nm_depol.add_all_qubit_quantum_error(
    pauli_error([('X', 0.033), ('Y', 0.033), ('Z', 0.034), ('I', 0.9)]), ['h'])

print("H|0⟩ then measure (should be ~50/50 for 0 and 1):")
for name, nm in [("No noise", None), ("Bit-flip 10%", nm_bitflip),
                  ("Phase-flip 10%", nm_phaseflip), ("Depolarizing 10%", nm_depol)]:
    if nm is None:
        sim = AerSimulator()
        counts = sim.run(qc, shots=10000, seed_simulator=42).result().get_counts()
    else:
        counts = run_noisy(qc, nm)
    zeros = counts.get('0', 0)
    ones = counts.get('1', 0)
    print(f"  {name:20s}: 0→{zeros/100:5.1f}%  1→{ones/100:5.1f}%")
