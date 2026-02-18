"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.6 Transpilation: From Your Circuit to the Hardware's
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_15_transpilation_from_your_circuit_to_the_h.py
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Your circuit: uses H, Toffoli (ccx)
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.ccx(0, 1, 2)  # Toffoli -- NOT a native gate on any current hardware
qc.measure([0, 1, 2], [0, 1, 2])

print("Your circuit:")
print(qc.draw())
print(f"Depth: {qc.depth()}, Gates: {dict(qc.count_ops())}")

# Transpile for a generic backend with basis gates {cx, id, rz, sx, x}
transpiled = transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'],
                       optimization_level=1, seed_transpiler=42)

print("\nTranspiled circuit:")
print(transpiled.draw())
print(f"Depth: {transpiled.depth()}, Gates: {dict(transpiled.count_ops())}")

# Verify they produce the same results
sim = AerSimulator()
result_orig = sim.run(qc, shots=10000, seed_simulator=42).result()
result_trans = sim.run(transpiled, shots=10000, seed_simulator=42).result()

print(f"\nOriginal:    {dict(sorted(result_orig.get_counts().items()))}")
print(f"Transpiled:  {dict(sorted(result_trans.get_counts().items()))}")
