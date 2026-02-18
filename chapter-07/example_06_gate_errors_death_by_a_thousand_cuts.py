"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.3 Gate Errors: Death by a Thousand Cuts
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_06_gate_errors_death_by_a_thousand_cuts.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np

# CNOT errors dominate: GHZ state fidelity vs qubit count
gate_error_1q = 0.0003
gate_error_2q = 0.002

noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(gate_error_1q, 1), ['h'])
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(gate_error_2q, 2), ['cx'])

sim = AerSimulator(noise_model=noise_model)

print("GHZ state fidelity vs. qubit count")
print(f"1-qubit error: {gate_error_1q*100:.2f}%, 2-qubit error: {gate_error_2q*100:.1f}%\n")

for n_qubits in [2, 3, 4, 5, 6, 8, 10, 15, 20]:
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(0, i + 1)
    qc.measure(range(n_qubits), range(n_qubits))

    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()

    # GHZ fidelity: fraction of correct outcomes (all-0s or all-1s)
    all_zeros = '0' * n_qubits
    all_ones = '1' * n_qubits
    correct = counts.get(all_zeros, 0) + counts.get(all_ones, 0)
    fidelity = correct / 10000
    n_cnots = n_qubits - 1

    print(f"  {n_qubits:2d} qubits ({n_cnots:2d} CNOTs): "
          f"fidelity = {fidelity:.3f}  "
          f"(wrong outcomes: {(1-fidelity)*100:.1f}%)")
