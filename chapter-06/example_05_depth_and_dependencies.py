"""Compare two equivalent GHZ preparations through depth and DAG layers."""

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.quantum_info import Statevector


chain = QuantumCircuit(4, name="chain")
chain.h(0)
chain.cx(0, 1)
chain.cx(1, 2)
chain.cx(2, 3)

tree = QuantumCircuit(4, name="tree")
tree.h(0)
tree.cx(0, 1)
tree.cx(0, 2)
tree.cx(1, 3)

print("chain depth:", chain.depth())
print("tree depth:", tree.depth())
print(
    "same prepared state:",
    Statevector.from_instruction(chain).equiv(Statevector.from_instruction(tree)),
)

dag = circuit_to_dag(tree)
for layer_index, layer in enumerate(dag.layers()):
    labels = []
    for node in layer["graph"].op_nodes():
        q_indices = [tree.find_bit(bit).index for bit in node.qargs]
        labels.append(f"{node.op.name}{q_indices}")
    print(f"layer {layer_index}:", labels)
