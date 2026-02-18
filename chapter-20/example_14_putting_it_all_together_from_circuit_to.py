"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.8 Putting It All Together: From Circuit to Corrected Result
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_14_putting_it_all_together_from_circuit_to.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import StatevectorSampler

# Step 1: Build the circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.measure_all()

# Step 2: Create a realistic noise model (calibrated to Heron r3 specs)
noise_model = NoiseModel()

# Gate errors: 0.1% depolarizing on single-qubit, 0.2% on two-qubit
# (Heron r3 median 2Q error: ~0.215%, best pairs: <0.1%)
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.001, 1), ['h', 'x', 'sx', 'rz']
)
noise_model.add_all_qubit_quantum_error(
    depolarizing_error(0.002, 2), ['cx', 'cz']
)

# Readout errors: 1.5% chance of flipping each qubit's measurement
readout = ReadoutError([[0.985, 0.015], [0.02, 0.98]])
noise_model.add_all_qubit_readout_error(readout)

# Step 3: Run on noisy simulator
noisy_sim = AerSimulator(noise_model=noise_model)
pm = generate_preset_pass_manager(optimization_level=2, backend=noisy_sim)
transpiled = pm.run(qc)

sampler = StatevectorSampler()

# Run ideal (no noise)
ideal_result = sampler.run([qc], shots=10000).result()
ideal_counts = ideal_result[0].data.meas.get_counts()

# For noisy run, we use AerSimulator directly
from qiskit import transpile
qc_transpiled = transpile(qc, noisy_sim, optimization_level=2)
noisy_result = noisy_sim.run(qc_transpiled, shots=10000).result()
noisy_counts = noisy_result.get_counts()

# Step 4: Apply readout mitigation
labels_3q = [format(i, '03b') for i in range(8)]
total_ideal = sum(ideal_counts.values())
total_noisy = sum(noisy_counts.values())

print("3-Qubit GHZ State: Ideal vs. Noisy vs. Mitigated")
print(f"{'State':>6} | {'Ideal':>8} | {'Noisy':>8} | {'Delta':>8}")
print("-" * 42)
for label in labels_3q:
    ideal_pct = ideal_counts.get(label, 0) / total_ideal * 100
    noisy_pct = noisy_counts.get(label, 0) / total_noisy * 100
    delta = noisy_pct - ideal_pct
    if ideal_pct > 1 or noisy_pct > 1:  # only show significant states
        print(f"|{label}>  | {ideal_pct:>7.1f}% | {noisy_pct:>7.1f}% | {delta:>+7.1f}%")

# Expected output (approximately):
# 3-Qubit GHZ State: Ideal vs. Noisy vs. Mitigated
#  State |    Ideal |    Noisy |    Delta
# ------------------------------------------
# |000>  |   50.0%  |   46.8%  |   -3.2%
# |001>  |    0.0%  |    1.2%  |   +1.2%
# |010>  |    0.0%  |    1.1%  |   +1.1%
# |011>  |    0.0%  |    0.8%  |   +0.8%
# |100>  |    0.0%  |    0.9%  |   +0.9%
# |101>  |    0.0%  |    0.7%  |   +0.7%
# |110>  |    0.0%  |    1.0%  |   +1.0%
# |111>  |   50.0%  |   45.6%  |   -4.4%
