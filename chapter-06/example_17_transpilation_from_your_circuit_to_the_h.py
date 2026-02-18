"""
Pre Quantum - Chapter 06: Quantum Circuits
Code Example: Beat 3: The Concept Build > 3.6 Transpilation: From Your Circuit to the Hardware's
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-06/example_17_transpilation_from_your_circuit_to_the_h.py
"""

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager

# Transpilation optimization levels
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.h(0)
qc.cx(0, 1)
qc.h(1)

print("Original circuit:")
print(qc.draw())
print(f"  Depth: {qc.depth()}, Gate count: {sum(qc.count_ops().values())}")

for opt_level in [0, 1, 2, 3]:
    pm = generate_preset_pass_manager(
        optimization_level=opt_level,
        basis_gates=['cx', 'id', 'rz', 'sx', 'x'],
        seed_transpiler_pass=42
    )
    t = pm.run(qc)
    gate_count = sum(t.count_ops().values())
    cx_count = t.count_ops().get('cx', 0)
    print(f"  Opt level {opt_level}: depth={t.depth():3d}, "
          f"gates={gate_count}, CX={cx_count}")
