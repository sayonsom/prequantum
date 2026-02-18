"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.3 Gate Errors: Death by a Thousand Cuts
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_05_gate_errors_death_by_a_thousand_cuts.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np

# How errors compound as circuits get deeper
# Using realistic 2025-era error rates
gate_error_1q = 0.0003   # 0.03% per single-qubit gate (IBM Heron r3 class)
gate_error_2q = 0.002    # 0.2% per two-qubit gate (good modern hardware)

noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(gate_error_1q, 1), ['h', 'x', 'z', 's', 't'])
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(gate_error_2q, 2), ['cx'])

sim = AerSimulator(noise_model=noise_model)

# Build increasingly deep circuits that should return |0⟩
# (Apply H twice = identity, so 2n Hadamards should give |0⟩)
print("Error accumulation: 2n Hadamards on 1 qubit (should always give |0⟩)")
print(f"Gate error: {gate_error_1q*100:.2f}% per H gate\n")

for n_pairs in [0, 10, 50, 100, 500, 1000]:
    qc = QuantumCircuit(1, 1)
    for _ in range(n_pairs):
        qc.h(0)
        qc.h(0)
    qc.measure(0, 0)

    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()
    prob_0 = counts.get('0', 0) / 10000
    n_gates = 2 * n_pairs
    # For depolarizing noise on 1 qubit with error p, each gate multiplies
    # the polarization by (1 - p). After n gates: F ≈ 0.5 + 0.5*(1-p)^n
    expected = 0.5 + 0.5 * (1 - gate_error_1q) ** n_gates

    print(f"  {n_gates:5d} gates: P(0) = {prob_0:.4f}  "
          f"(theory ≈ {expected:.4f})")
