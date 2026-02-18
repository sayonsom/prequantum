"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.2 The Translation Pattern: Thinking in Gates, Not SDKs
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_03_the_translation_pattern_thinking_in_gate.py
"""

# Parameterized circuit in all three SDKs
import numpy as np

# === Qiskit: parameters are symbolic objects ===
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
theta = Parameter('θ')
qc_param = QuantumCircuit(1, 1)
qc_param.ry(theta, 0)
qc_param.measure(0, 0)
# Bind later: qc_param.assign_parameters({theta: np.pi/4})

# === Cirq: parameters use sympy ===
import cirq, sympy
theta_cirq = sympy.Symbol('θ')
q = cirq.LineQubit(0)
circuit_param = cirq.Circuit([
    cirq.ry(theta_cirq)(q),
    cirq.measure(q, key='m')
])
# Resolve later: cirq.resolve_parameters(circuit_param, {'θ': np.pi/4})

# === PennyLane: parameters are just function arguments ===
import pennylane as qml
dev1 = qml.device('default.qubit', wires=1, shots=1024)

@qml.qnode(dev1)
def param_circuit(theta):
    qml.RY(theta, wires=0)
    return qml.counts()

# Call directly: param_circuit(np.pi/4)
result = param_circuit(np.pi / 4)
print("PennyLane parameterized:", result)
# Output: {'0': ~854, '1': ~170}
