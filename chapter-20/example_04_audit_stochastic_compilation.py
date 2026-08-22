"""Compile with several seeds and retain a transparent selection record."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.transpiler import generate_preset_pass_manager


coupling_map = []
for left in range(7):
    coupling_map.extend(([left, left + 1], [left + 1, left]))
backend = GenericBackendV2(
    num_qubits=8,
    basis_gates=["rz", "sx", "x", "cz"],
    coupling_map=coupling_map,
    seed=19,
)

circuit = QuantumCircuit(8)
circuit.h(range(8))
for control, target in (
    (0, 7), (1, 6), (2, 5), (3, 4),
    (0, 4), (7, 3), (1, 5), (6, 2),
    (0, 6), (7, 1), (2, 4), (5, 3),
):
    circuit.cx(control, target)
circuit.measure_all()

records = []
for seed in range(10):
    manager = generate_preset_pass_manager(
        optimization_level=2,
        backend=backend,
        seed_transpiler=seed,
    )
    compiled = manager.run(circuit)
    operations = dict(compiled.count_ops())
    records.append(
        {
            "seed": seed,
            "depth": compiled.depth(),
            "cz": operations.get("cz", 0),
            "size": compiled.size(),
        }
    )

best = min(records, key=lambda record: (record["cz"], record["depth"], record["size"]))

for record in records:
    print(record)
print("Selected by (CZ count, depth, size):", best)

assert best in records
assert len({record["seed"] for record in records}) == 10
