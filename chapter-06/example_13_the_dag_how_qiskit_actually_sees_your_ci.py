"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.5 The DAG: How Qiskit Actually Sees Your Circuit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_13_the_dag_how_qiskit_actually_sees_your_ci.py
"""

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

# Build a circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)
qc.cx(0, 1)
qc.cx(1, 2)
qc.h(2)

# Convert to DAG
dag = circuit_to_dag(qc)

# Inspect the DAG structure
print(f"DAG nodes (operations): {dag.size()}")
print(f"DAG depth: {dag.depth()}")
print(f"DAG width: {dag.width()}")  # qubits + classical bits

# List all operation nodes
for node in dag.topological_op_nodes():
    print(f"  {node.name} on qubits {[q._index for q in node.qargs]}")

# The topological ordering respects dependencies:
# H(0) and H(1) can be parallel -- no shared qubit
# CX(0,1) must wait for both H(0) and H(1) to finish
# CX(1,2) must wait for CX(0,1)
# H(2) can run in parallel with anything not touching qubit 2
