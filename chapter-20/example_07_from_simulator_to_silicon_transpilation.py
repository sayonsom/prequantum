"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.4 From Simulator to Silicon: Transpilation Deep Dive
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_07_from_simulator_to_silicon_transpilation.py
"""

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import CouplingMap

# Our abstract circuit: 3-qubit GHZ state
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)   # assumes qubit 0 connects to qubit 2
qc.measure([0, 1, 2], [0, 1, 2])

print("Abstract circuit (what you wrote):")
print(qc.draw())
print(f"Depth: {qc.depth()}, Gates: {dict(qc.count_ops())}")
# Depth: 4, Gates: {'h': 1, 'cx': 2, 'measure': 3}

# Transpile for a backend with limited connectivity
# Simulate a 5-qubit device where qubits connect in a line: 0-1-2-3-4
coupling = CouplingMap([(0,1), (1,0), (1,2), (2,1), (2,3), (3,2), (3,4), (4,3)])

# Compare optimization levels
# Note: Heron r2/r3 native basis uses CZ, not CX
for opt_level in [0, 1, 2, 3]:
    pm = generate_preset_pass_manager(
        optimization_level=opt_level,
        coupling_map=coupling,
        basis_gates=['cz', 'rz', 'sx', 'x', 'id'],  # Heron r2/r3 basis
        seed_transpiler=42  # reproducibility!
    )
    transpiled = pm.run(qc)
    ops = dict(transpiled.count_ops())
    cz_count = ops.get('cz', 0)
    print(f"  Level {opt_level}: depth={transpiled.depth():>3}, "
          f"CZ={cz_count}, total_gates={sum(v for k,v in ops.items() if k != 'measure')}")

# Typical output:
#   Level 0: depth= 17, CZ=8, total_gates=19
#   Level 1: depth= 12, CZ=6, total_gates=14
#   Level 2: depth= 10, CZ=5, total_gates=12
#   Level 3: depth=  9, CZ=4, total_gates=11
