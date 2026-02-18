"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.2 Running Circuits: Simulators, Shots, and the Primitives API
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_05_running_circuits_simulators_shots_and_th.py
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Build circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Use the Sampler primitive
sampler = StatevectorSampler(seed=42)

# Primitives use "PUBs" -- Primitive Unified Blocs
# A sampler PUB is: (circuit, <optional params>, <optional shots>)
job = sampler.run([(qc,)], shots=10000)
result = job.result()

# Access results -- V2 primitives return structured data
pub_result = result[0]  # first PUB's result
counts = pub_result.data.meas.get_counts()
print(f"Sampler results: {counts}")
# {'00': ~5000, '11': ~5000}
