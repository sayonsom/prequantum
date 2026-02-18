"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.2 Running Circuits: Simulators, Shots, and the Primitives API
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_06_running_circuits_simulators_shots_and_th.py
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# Estimator: compute expectation values
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Define an observable: Z⊗Z (measures correlation between qubits)
observable = SparsePauliOp("ZZ")

estimator = StatevectorEstimator()
job = estimator.run([(qc, observable)])
result = job.result()

print(f"⟨ZZ⟩ = {result[0].data.evs:.4f}")
# 1.0 -- perfect correlation (both qubits always agree)

# Compare: uncorrelated qubits
qc_uncorr = QuantumCircuit(2)
qc_uncorr.h(0)
qc_uncorr.h(1)  # independent superpositions, no entanglement

job2 = estimator.run([(qc_uncorr, observable)])
result2 = job2.result()
print(f"⟨ZZ⟩ (uncorrelated) = {result2[0].data.evs:.4f}")
# 0.0 -- no correlation
