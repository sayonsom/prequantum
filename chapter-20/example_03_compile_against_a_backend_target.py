"""Compile an abstract circuit against a reproducible BackendV2 target."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.transpiler import generate_preset_pass_manager


coupling_map = [
    [0, 1], [1, 0],
    [1, 2], [2, 1],
    [2, 3], [3, 2],
    [3, 4], [4, 3],
]
backend = GenericBackendV2(
    num_qubits=5,
    basis_gates=["rz", "sx", "x", "cz"],
    coupling_map=coupling_map,
    seed=11,
)

intent_circuit = QuantumCircuit(3)
intent_circuit.h(0)
intent_circuit.cx(0, 1)
intent_circuit.cx(0, 2)
intent_circuit.measure_all()

pass_manager = generate_preset_pass_manager(
    optimization_level=1,
    backend=backend,
    seed_transpiler=13,
)
isa_circuit = pass_manager.run(intent_circuit)

supported = set(backend.target.operation_names)
compiled_operations = set(isa_circuit.count_ops())
# A barrier is a compiler directive, not an operation executed by the backend.
compiled_operations.discard("barrier")
unsupported = compiled_operations - supported

print("Intent operations: ", dict(intent_circuit.count_ops()))
print("Target operations: ", sorted(supported))
print("Compiled operations:", dict(isa_circuit.count_ops()))
print("Compiled depth:     ", isa_circuit.depth())
print("Layout present:     ", isa_circuit.layout is not None)

assert isa_circuit.num_qubits == backend.num_qubits
assert unsupported == set()
