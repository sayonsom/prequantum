"""Separate an exact simulator calculation from a finite-shot sample."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector


bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)

exact_raw = Statevector.from_instruction(bell).probabilities_dict()
exact = {str(key): float(value) for key, value in exact_raw.items()}

measured = bell.copy()
measured.measure_all()
shots = 1000
sampled = StatevectorSampler(seed=21).run([measured], shots=shots).result()
counts = sampled[0].data.meas.get_counts()
frequencies = {key: value / shots for key, value in sorted(counts.items())}

print("Exact probabilities:", {key: round(value, 3) for key, value in exact.items()})
print("Finite-shot counts:  ", counts)
print("Finite frequencies:  ", {key: round(value, 3) for key, value in frequencies.items()})

assert set(exact) == {"00", "11"}
assert abs(exact["00"] - 0.5) < 1e-12
assert abs(exact["11"] - 0.5) < 1e-12
assert sum(counts.values()) == shots
