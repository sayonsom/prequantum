"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.4 Circuit Depth: Why It Matters
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_11_circuit_depth_why_it_matters.py
"""

from qiskit import QuantumCircuit

# Shallow circuit: gates on different qubits run in parallel
shallow = QuantumCircuit(3)
shallow.h(0)    # Time step 1: all three H gates
shallow.h(1)    #   run simultaneously
shallow.h(2)
print(f"Parallel H gates:")
print(shallow.draw())
print(f"Depth: {shallow.depth()}")  # 1 -- all parallel!

# Deep circuit: gates on the same qubit must be sequential
deep = QuantumCircuit(1)
deep.h(0)       # Step 1
deep.t(0)       # Step 2
deep.h(0)       # Step 3
deep.t(0)       # Step 4
deep.h(0)       # Step 5
print(f"\nSequential gates:")
print(deep.draw())
print(f"Depth: {deep.depth()}")  # 5 -- all sequential

# Mixed: some parallel, some sequential
mixed = QuantumCircuit(3)
mixed.h(0)       # Step 1: H on q0
mixed.h(1)       # Step 1: H on q1 (parallel with above)
mixed.cx(0, 1)   # Step 2: CNOT (needs both q0 and q1)
mixed.h(2)       # Step 2: H on q2 (parallel with CNOT)
mixed.cx(1, 2)   # Step 3: CNOT q1→q2
print(f"\nMixed circuit:")
print(mixed.draw())
print(f"Depth: {mixed.depth()}")  # 3
