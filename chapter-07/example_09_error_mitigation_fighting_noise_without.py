"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.6 Error Mitigation: Fighting Noise Without Error Correction
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_09_error_mitigation_fighting_noise_without.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError
import numpy as np

# Simulate measurement errors
# P(read 1 | state is 0) = 2%, P(read 0 | state is 1) = 3%
readout_error = ReadoutError([[0.98, 0.02], [0.03, 0.97]])

noise_model = NoiseModel()
noise_model.add_all_qubit_readout_error(readout_error)

sim = AerSimulator(noise_model=noise_model)

# Step 1: CALIBRATE -- prepare known states and measure
# Prepare |0⟩, measure
qc0 = QuantumCircuit(1, 1)
qc0.measure(0, 0)
counts0 = sim.run(qc0, shots=10000, seed_simulator=42).result().get_counts()

# Prepare |1⟩, measure
qc1 = QuantumCircuit(1, 1)
qc1.x(0)
qc1.measure(0, 0)
counts1 = sim.run(qc1, shots=10000, seed_simulator=42).result().get_counts()

print("Step 1: Calibration measurements")
print(f"  Prepared |0⟩: {counts0}")
print(f"  Prepared |1⟩: {counts1}")

# Step 2: BUILD the calibration matrix
# M[i][j] = P(read i | state is j)
p_read0_given0 = counts0.get('0', 0) / 10000
p_read1_given0 = counts0.get('1', 0) / 10000
p_read0_given1 = counts1.get('0', 0) / 10000
p_read1_given1 = counts1.get('1', 0) / 10000

M = np.array([
    [p_read0_given0, p_read0_given1],
    [p_read1_given0, p_read1_given1]
])
print(f"\nStep 2: Calibration matrix M:")
print(f"  {np.round(M, 4)}")
print(f"  (Columns are true states, rows are read outcomes)")

# Step 3: RUN the real experiment -- Bell state with readout errors
qc_bell = QuantumCircuit(2, 2)
qc_bell.h(0)
qc_bell.cx(0, 1)
qc_bell.measure([0, 1], [0, 1])

result_bell = sim.run(qc_bell, shots=10000, seed_simulator=42).result()
noisy_counts = result_bell.get_counts()
print(f"\nStep 3: Noisy Bell state: {dict(sorted(noisy_counts.items()))}")

# Step 4: MITIGATE -- solve M_full @ ideal_probs = noisy_probs
# For 2 qubits, the full calibration matrix is M ⊗ M (tensor product)
M_full = np.kron(M, M)  # 4x4 calibration matrix
noisy_probs = np.array([noisy_counts.get(f'{i:02b}', 0) / 10000
                         for i in range(4)])

# Invert the calibration matrix to get mitigated probabilities
M_inv = np.linalg.inv(M_full)
mitigated_probs = M_inv @ noisy_probs

# Clip negative values (can happen with matrix inversion)
mitigated_probs = np.maximum(mitigated_probs, 0)
mitigated_probs = mitigated_probs / mitigated_probs.sum()

print(f"\nStep 4: Correction (apply M⁻¹)")
print(f"  Noisy probs:     {np.round(noisy_probs, 4)}")
print(f"  Mitigated probs: {np.round(mitigated_probs, 4)}")
print(f"  Ideal probs:     [0.5, 0.0, 0.0, 0.5]")
