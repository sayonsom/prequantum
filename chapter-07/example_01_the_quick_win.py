"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# A Bell state circuit -- should give ONLY 00 and 11
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# --- Perfect simulation ---
sim_perfect = AerSimulator()
result_perfect = sim_perfect.run(qc, shots=10000, seed_simulator=42).result()
counts_perfect = result_perfect.get_counts()

# --- Noisy simulation ---
noise_model = NoiseModel()
# 0.1% error on single-qubit gates (typical IBM Heron r3)
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.001, 1), ['h'])
# 0.5% error on two-qubit gates (good modern hardware)
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.005, 2), ['cx'])

sim_noisy = AerSimulator(noise_model=noise_model)
result_noisy = sim_noisy.run(qc, shots=10000, seed_simulator=42).result()
counts_noisy = result_noisy.get_counts()

print("Perfect simulator:")
for k in sorted(counts_perfect):
    print(f"  {k}: {counts_perfect[k]:5d}  ({counts_perfect[k]/100:.1f}%)")

print("\nNoisy simulator (0.1% single-gate, 0.5% CX error):")
for k in sorted(counts_noisy):
    print(f"  {k}: {counts_noisy[k]:5d}  ({counts_noisy[k]/100:.1f}%)")
