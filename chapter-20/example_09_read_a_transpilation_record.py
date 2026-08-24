"""Read a transpilation through layout, target, measurement, and evidence records."""

from __future__ import annotations

from collections import defaultdict
import json

from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.quantum_info import Statevector
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator


backend = GenericBackendV2(
    num_qubits=3,
    basis_gates=["rz", "sx", "x", "cz"],
    coupling_map=[[0, 1], [1, 0], [1, 2], [2, 1]],
    seed=41,
)

intent = QuantumCircuit(2, 2)
intent.h(0)
intent.cx(0, 1)
intent.measure([0, 1], [0, 1])

manager = generate_preset_pass_manager(
    optimization_level=2,
    backend=backend,
    seed_transpiler=20,
    initial_layout=[0, 2],
)
isa_circuit = manager.run(intent)

# Read the representation change, rather than comparing drawings gate by gate.
initial_layout = isa_circuit.layout.initial_index_layout(filter_ancillas=True)
final_layout = isa_circuit.layout.final_index_layout(filter_ancillas=True)
measurement_map = {}
for instruction in isa_circuit.data:
    if instruction.operation.name == "measure":
        physical = isa_circuit.find_bit(instruction.qubits[0]).index
        classical = isa_circuit.find_bit(instruction.clbits[0]).index
        measurement_map[classical] = physical

compiled_operations = set(isa_circuit.count_ops()) - {"barrier"}
assert compiled_operations <= set(backend.target.operation_names)
assert initial_layout == [0, 2]
assert final_layout == [0, 1]
assert measurement_map == {0: 0, 1: 1}

# Verify the declared input-and-measurement contract exactly on a statevector.
before_measurement = isa_circuit.remove_final_measurements(inplace=False)
state = Statevector.from_instruction(before_measurement)
exact_distribution: defaultdict[str, float] = defaultdict(float)
for physical_basis, probability in state.probabilities_dict().items():
    classical_bits = ["0"] * intent.num_clbits
    for classical, physical in measurement_map.items():
        classical_bits[classical] = physical_basis[-1 - physical]
    classical_key = "".join(reversed(classical_bits))
    exact_distribution[classical_key] += float(probability)

exact_distribution = defaultdict(
    float,
    {
        key: value
        for key, value in exact_distribution.items()
        if value > 1e-12
    },
)
assert set(exact_distribution) == {"00", "11"}
assert abs(exact_distribution["00"] - 0.5) < 1e-12
assert abs(exact_distribution["11"] - 0.5) < 1e-12

# A finite-shot execution is a separate record from the exact check.
shots = 2048
counts = AerSimulator().run(
    isa_circuit,
    shots=shots,
    seed_simulator=23,
).result().get_counts()
assert sum(counts.values()) == shots
assert set(counts) <= {"00", "11"}

record = {
    "intent_operations": dict(intent.count_ops()),
    "target_operations": sorted(backend.target.operation_names),
    "initial_layout_logical_to_physical": initial_layout,
    "final_layout_logical_to_physical": final_layout,
    "measurement_map_classical_to_physical": measurement_map,
    "isa_operations": dict(isa_circuit.count_ops()),
    "isa_depth": isa_circuit.depth(),
    "exact_output_distribution": dict(sorted(exact_distribution.items())),
    "finite_shot_counts": dict(sorted(counts.items())),
}
print(json.dumps(record, indent=2))
