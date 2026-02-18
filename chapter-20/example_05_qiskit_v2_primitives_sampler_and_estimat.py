"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.3 Qiskit V2 Primitives: Sampler and Estimator
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_05_qiskit_v2_primitives_sampler_and_estimat.py
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
import numpy as np

# Build a simple circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# --- SamplerV2: "What did I measure?" ---
qc_meas = qc.copy()
qc_meas.measure_all()

sampler = StatevectorSampler()
job = sampler.run([qc_meas], shots=4096)
result = job.result()
counts = result[0].data.meas.get_counts()
print("SamplerV2 counts:", counts)
# Output: {'00': 2048, '11': 2048}

# --- EstimatorV2: "What's the average?" ---
# Measure the ZZ observable: are the qubits correlated?
observable = SparsePauliOp('ZZ')

estimator = StatevectorEstimator()
job_est = estimator.run([(qc, observable)])
result_est = job_est.result()
print(f"EstimatorV2 <ZZ>: {result_est[0].data.evs[0]:.4f}")
# Output: EstimatorV2 <ZZ>: 1.0000
# <ZZ> = 1 means perfect correlation: both qubits always match

# Compare with an uncorrelated state (just H on qubit 0, no CNOT)
qc_uncorr = QuantumCircuit(2)
qc_uncorr.h(0)
job_uncorr = estimator.run([(qc_uncorr, observable)])
result_uncorr = job_uncorr.result()
print(f"EstimatorV2 <ZZ> (uncorrelated): {result_uncorr[0].data.evs[0]:.4f}")
# Output: EstimatorV2 <ZZ> (uncorrelated): 0.0000
# <ZZ> = 0 means no correlation
