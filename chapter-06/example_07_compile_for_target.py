"""Compile an abstract circuit against an explicit target and verify equivalence."""

from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.quantum_info import Operator
from qiskit.transpiler import CouplingMap, generate_preset_pass_manager


backend = GenericBackendV2(
    num_qubits=4,
    basis_gates=["rz", "sx", "x", "cx"],
    coupling_map=CouplingMap.from_line(4),
    seed=11,
)

logical = QuantumCircuit(4, name="logical")
logical.h(0)
logical.cx(0, 3)
logical.cx(3, 2)

pass_manager = generate_preset_pass_manager(
    optimization_level=1,
    backend=backend,
    initial_layout=[0, 1, 2, 3],
    seed_transpiler=11,
)
isa_circuit = pass_manager.run(logical)

target_names = backend.target.operation_names
unsupported = []
for instruction in isa_circuit.data:
    qargs = tuple(isa_circuit.find_bit(bit).index for bit in instruction.qubits)
    if not backend.target.instruction_supported(
        operation_name=instruction.operation.name,
        qargs=qargs,
    ):
        unsupported.append((instruction.operation.name, qargs))

print("target operation names:", sorted(target_names))
print("all compiled operations supported at assigned qubits:", not unsupported)
print(
    "equivalent with layout applied:",
    Operator.from_circuit(logical).equiv(Operator.from_circuit(isa_circuit)),
)
print("logical depth:", logical.depth())
print("compiled depth:", isa_circuit.depth())

assert not unsupported
assert Operator.from_circuit(logical).equiv(Operator.from_circuit(isa_circuit))
