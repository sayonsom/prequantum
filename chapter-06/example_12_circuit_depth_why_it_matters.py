"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.4 Circuit Depth: Why It Matters
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_12_circuit_depth_why_it_matters.py
"""

from qiskit import QuantumCircuit

# Two circuits that do the same thing, different depths
# Version 1: sequential CNOTs (depth grows linearly)
linear = QuantumCircuit(4)
linear.h(0)
linear.cx(0, 1)
linear.cx(1, 2)
linear.cx(2, 3)
print(f"Linear CNOT chain: depth = {linear.depth()}")  # 4

# Version 2: tree structure (depth grows logarithmically)
tree = QuantumCircuit(4)
tree.h(0)
tree.cx(0, 1)   # Step 2: parallel
tree.cx(0, 2)   # Step 3
tree.cx(0, 3)   # Step 4
print(f"Star CNOT pattern: depth = {tree.depth()}")  # 4

# For GHZ state specifically, a log-depth version exists:
ghz_log = QuantumCircuit(4)
ghz_log.h(0)
ghz_log.cx(0, 1)  # Step 2
ghz_log.cx(0, 2)  # Step 3 (parallel with next if hardware allows)
ghz_log.cx(1, 3)  # Step 3 (parallel with previous)
print(f"Log-depth GHZ: depth = {ghz_log.depth()}")  # 3

print(f"\nLog-depth GHZ circuit:")
print(ghz_log.draw())
