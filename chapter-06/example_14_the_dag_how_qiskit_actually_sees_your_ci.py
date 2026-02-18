"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.5 The DAG: How Qiskit Actually Sees Your Circuit
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_14_the_dag_how_qiskit_actually_sees_your_ci.py
"""

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit

# The DAG reveals optimization opportunities
qc = QuantumCircuit(1)
qc.h(0)
qc.h(0)  # H*H = I, these cancel
qc.x(0)
qc.x(0)  # X*X = I, these cancel too

dag = circuit_to_dag(qc)
print(f"Before optimization: {dag.size()} ops, depth {dag.depth()}")

# Manual cancellation (the transpiler does this automatically)
# In practice, use the InverseCancellation pass
from qiskit.transpiler.passes import InverseCancellation
from qiskit.circuit.library import HGate, XGate

cancellation = InverseCancellation([(HGate(), HGate()), (XGate(), XGate())])
optimized_dag = cancellation.run(dag)
optimized_qc = dag_to_circuit(optimized_dag)

print(f"After optimization: {optimized_dag.size()} ops, depth {optimized_dag.depth()}")
print(optimized_qc.draw())
# Empty circuit -- all gates cancelled!
