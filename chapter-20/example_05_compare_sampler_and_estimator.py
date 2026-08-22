"""Use SamplerV2 and EstimatorV2 for two different evidence questions."""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator, StatevectorSampler
from qiskit.quantum_info import SparsePauliOp


state_preparation = QuantumCircuit(2)
state_preparation.h(0)
state_preparation.cx(0, 1)

measured = state_preparation.copy()
measured.measure_all()
sampler_job = StatevectorSampler(seed=31).run([measured], shots=2048)
sampler_result = sampler_job.result()[0]
counts = sampler_result.data.meas.get_counts()

observable = SparsePauliOp.from_list([("ZZ", 1.0)])
estimator_job = StatevectorEstimator(seed=31).run(
    [(state_preparation, observable)]
)
estimator_result = estimator_job.result()[0]
zz_expectation = float(np.asarray(estimator_result.data.evs).reshape(-1)[0])

print("Sampler evidence (bitstrings):", counts)
print("Estimator evidence (<ZZ>):    ", round(zz_expectation, 6))
print("Sampler metadata keys:        ", sorted(sampler_result.metadata))
print("Estimator metadata keys:      ", sorted(estimator_result.metadata))

assert set(counts) <= {"00", "11"}
assert np.isclose(zz_expectation, 1.0)

