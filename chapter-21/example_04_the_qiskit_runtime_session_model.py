"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.4 The Qiskit Runtime Session Model
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_04_the_qiskit_runtime_session_model.py
"""

from qiskit_ibm_runtime import (
    QiskitRuntimeService, Session,
    SamplerV2 as Sampler, EstimatorV2 as Estimator
)
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
import numpy as np

service = QiskitRuntimeService(channel="ibm_quantum")
backend = service.least_busy(min_num_qubits=4, operational=True)

# A session = a managed connection to a specific backend
# All jobs in the session skip the queue after the first
with Session(service=service, backend=backend) as session:

    # Job 1: Sample a GHZ state
    sampler = Sampler(session=session)
    ghz = QuantumCircuit(4)
    ghz.h(0)
    for i in range(1, 4):
        ghz.cx(0, i)
    ghz.measure_all()

    sample_job = sampler.run([ghz], shots=4096)
    print(f"Sampler job: {sample_job.job_id()}")

    # Job 2: Estimate <ZZ> on the same backend (no re-queuing!)
    estimator = Estimator(session=session)
    bell = QuantumCircuit(2)
    bell.h(0)
    bell.cx(0, 1)

    observable = SparsePauliOp("ZZ")
    estimate_job = estimator.run([(bell, observable)])
    print(f"Estimator job: {estimate_job.job_id()}")

    # Both jobs ran on the same backend without waiting in queue again
    sample_result = sample_job.result()
    estimate_result = estimate_job.result()

    print(f"GHZ counts: {sample_result[0].data.meas.get_counts()}")
    print(f"<ZZ> = {estimate_result[0].data.evs[0]:.4f}")

# Session closes automatically -- backend released back to pool
# Expected output:
# Sampler job: cr5x7k2...
# Estimator job: cr5x7k3...
# GHZ counts: {'0000': 2012, '1111': 2084}
# <ZZ> = 0.9823
