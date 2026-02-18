"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.10 Circuit Composition and Reuse
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_26_circuit_composition_and_reuse.py
"""

from qiskit import QuantumCircuit

# Define a reusable Bell pair creator
def bell_pair() -> QuantumCircuit:
    qc = QuantumCircuit(2, name="Bell")
    qc.h(0)
    qc.cx(0, 1)
    return qc

# Convert to a gate (encapsulates the sub-circuit)
bell_gate = bell_pair().to_gate()

# Use it in a larger circuit
main = QuantumCircuit(4, 4)
main.append(bell_gate, [0, 1])  # Bell pair on qubits 0,1
main.append(bell_gate, [2, 3])  # Bell pair on qubits 2,3
main.measure_all()

print(main.draw())
print(f"Depth: {main.depth()}")

# Decompose to see the internals
decomposed = main.decompose()
print("\nDecomposed:")
print(decomposed.draw())
