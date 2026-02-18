"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.6 Transpilation: From Your Circuit to the Hardware's
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_18_transpilation_from_your_circuit_to_the_h.py
"""

from qiskit import QuantumCircuit, transpile

# Hadamard decomposition into Heron's native gates
qc = QuantumCircuit(1)
qc.h(0)

# Heron native gates: ECR, RZ, SX, X
transpiled = transpile(qc, basis_gates=['ecr', 'rz', 'sx', 'x'],
                       optimization_level=0, seed_transpiler=42)
print("H gate decomposed into native gates:")
print(transpiled.draw())
# H = Rz(π/2) · SX · Rz(π/2)  (up to global phase)

# Why this decomposition? Because:
# - Rz is a "virtual" gate -- it's just a software frame change, costs zero time
# - SX is a single microwave pulse, very fast (~20-30 ns)
# - So H costs exactly one physical pulse, the rest is bookkeeping
