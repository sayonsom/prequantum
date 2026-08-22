"""Compose a parameterized circuit template and evaluate a parameter sweep."""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp


theta = Parameter("theta")
feature = QuantumCircuit(1, name="feature")
feature.ry(theta, 0)

model = QuantumCircuit(2, name="model")
model.compose(feature, qubits=[0], inplace=True)
model.cx(0, 1)

parameter_values = [0.0, np.pi / 2, np.pi]
observable = SparsePauliOp("IZ")  # Z on q[0]; Pauli labels display q[0] at right.
result = (
    StatevectorEstimator()
    .run([(model, [observable], parameter_values)])
    .result()[0]
)

print("free parameters:", [parameter.name for parameter in model.parameters])
print("bound values:", parameter_values)
print("<Z on q[0]>:", result.data.evs)

assert np.allclose(result.data.evs, [1.0, 0.0, -1.0])
