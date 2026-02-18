"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.6 Transpilation: From Your Circuit to the Hardware's
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_16_transpilation_from_your_circuit_to_the_h.py
"""

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager, CouplingMap

# Build a circuit
qc = QuantumCircuit(4)
qc.h(0)
qc.cx(0, 3)  # qubit 0 talks to qubit 3 -- but are they connected?
qc.cx(1, 2)
qc.cx(2, 3)

# Define a linear coupling map: 0-1-2-3 (only neighbors can interact)
coupling = CouplingMap([(0,1), (1,0), (1,2), (2,1), (2,3), (3,2)])

# Use the staged pass manager
pm = generate_preset_pass_manager(
    optimization_level=2,
    basis_gates=['cx', 'rz', 'sx', 'x'],
    coupling_map=coupling
)

# Transpile
transpiled = pm.run(qc)

print("Original:")
print(qc.draw())
print(f"  Depth: {qc.depth()}, CX count: {qc.count_ops().get('cx', 0)}")

print("\nTranspiled (for linear coupling 0-1-2-3):")
print(transpiled.draw())
print(f"  Depth: {transpiled.depth()}, CX count: {transpiled.count_ops().get('cx', 0)}")

# Notice: CX(0,3) required SWAP insertion because 0 and 3 aren't connected.
# The transpiler inserted SWAP gates to route qubit 0's state next to qubit 3.
