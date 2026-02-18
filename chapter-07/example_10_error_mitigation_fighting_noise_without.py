"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.6 Error Mitigation: Fighting Noise Without Error Correction
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_10_error_mitigation_fighting_noise_without.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np

# The idea: run at noise level λ, 2λ, 3λ, then extrapolate to λ=0

base_error_2q = 0.01   # 1% base CX error (intentionally higher for demo)
base_error_1q = 0.001

# Bell state circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Measure the expectation value (fraction of correct outcomes) at noise scales
noise_scales = [1.0, 1.5, 2.0, 3.0]
expectation_values = []

print("Zero-Noise Extrapolation (ZNE)")
print(f"Base noise: {base_error_2q*100:.1f}% CX, {base_error_1q*100:.1f}% 1q\n")

for scale in noise_scales:
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(
        depolarizing_error(base_error_2q * scale, 2), ['cx'])
    nm.add_all_qubit_quantum_error(
        depolarizing_error(base_error_1q * scale, 1), ['h'])

    sim = AerSimulator(noise_model=nm)
    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()

    # Expectation: fraction of correct outcomes (00 or 11)
    correct = counts.get('00', 0) + counts.get('11', 0)
    ev = correct / 10000
    expectation_values.append(ev)
    print(f"  Noise scale {scale:.1f}x: correct = {ev:.4f}")

# Linear extrapolation to noise_scale = 0
coeffs_lin = np.polyfit(noise_scales, expectation_values, 1)
extrap_linear = np.polyval(coeffs_lin, 0)

# Quadratic extrapolation (often more accurate)
coeffs_quad = np.polyfit(noise_scales, expectation_values, 2)
extrap_quad = np.polyval(coeffs_quad, 0)

print(f"\nExtrapolated (linear):    {extrap_linear:.4f}")
print(f"Extrapolated (quadratic): {extrap_quad:.4f}")
print(f"Ideal value:              1.0000")
print(f"Best single measurement:  {expectation_values[0]:.4f}")
print(f"Improvement (linear):     {(extrap_linear - expectation_values[0]):.4f}")
print(f"Improvement (quadratic):  {(extrap_quad - expectation_values[0]):.4f}")
