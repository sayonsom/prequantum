"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.2 T1 and T2: How Fast Qubits Die
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_03_t1_and_t2_how_fast_qubits_die.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
import numpy as np

# Realistic T1/T2 values for a modern superconducting qubit
t1 = 200e-6       # 200 microseconds (IBM Heron-class)
t2 = 120e-6       # 120 microseconds
gate_time = 36e-9  # 36 nanoseconds per single-qubit gate

# Simulate the effect of waiting different amounts of time
# We model "waiting" as a series of identity gates, each costing gate_time
print("T1 relaxation: qubit starts in |1⟩, decays over time")
print(f"T1 = {t1*1e6:.0f} μs, T2 = {t2*1e6:.0f} μs, gate = {gate_time*1e9:.0f} ns\n")

for n_waits in [0, 100, 500, 1000, 3000, 5000]:
    wait_time = n_waits * gate_time

    # Create noise model with thermal relaxation
    noise_model = NoiseModel()
    error = thermal_relaxation_error(t1, t2, wait_time)
    noise_model.add_all_qubit_quantum_error(error, ['id'])

    # Prepare |1⟩, wait, measure
    qc = QuantumCircuit(1, 1)
    qc.x(0)       # Prepare |1⟩
    if n_waits > 0:
        qc.id(0)   # One identity gate representing the wait
    qc.measure(0, 0)

    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()
    prob_1 = counts.get('1', 0) / 10000
    expected = np.exp(-wait_time / t1)

    print(f"  Wait {wait_time*1e6:6.1f} μs: P(still |1⟩) = {prob_1:.3f}  "
          f"(theory: {expected:.3f})")
