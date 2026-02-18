"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.2 T1 and T2: How Fast Qubits Die
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_04_t1_and_t2_how_fast_qubits_die.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
import numpy as np

# T2 dephasing: superposition quality degrades over time
t1 = 200e-6
t2 = 120e-6
gate_time = 36e-9

print("T2 dephasing: qubit starts in |+⟩, phase coherence decays")
print(f"T1 = {t1*1e6:.0f} μs, T2 = {t2*1e6:.0f} μs\n")

for n_waits in [0, 100, 500, 1000, 3000, 5000]:
    wait_time = n_waits * gate_time

    noise_model = NoiseModel()
    error = thermal_relaxation_error(t1, t2, wait_time)
    noise_model.add_all_qubit_quantum_error(error, ['id'])

    # Prepare |+⟩, wait, measure in X basis (apply H then measure Z)
    qc = QuantumCircuit(1, 1)
    qc.h(0)       # Prepare |+⟩
    if n_waits > 0:
        qc.id(0)   # Wait
    qc.h(0)        # Change to X basis
    qc.measure(0, 0)

    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(qc, shots=10000, seed_simulator=42).result()
    counts = result.get_counts()
    # P(0) should be 1.0 for perfect |+⟩ → H → |0⟩
    prob_0 = counts.get('0', 0) / 10000
    expected = 0.5 + 0.5 * np.exp(-wait_time / t2)

    print(f"  Wait {wait_time*1e6:6.1f} μs: P(0) = {prob_0:.3f}  "
          f"(theory: {expected:.3f})")
