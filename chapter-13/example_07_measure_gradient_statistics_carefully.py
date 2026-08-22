import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector


layer_count = 3
sample_count = 32
parameter_shift = np.pi / 2.0


def prepare_state(width, parameters):
    circuit = QuantumCircuit(width)
    cursor = 0
    for _ in range(layer_count):
        for qubit in range(width):
            circuit.ry(float(parameters[cursor]), qubit)
            cursor += 1
            circuit.rz(float(parameters[cursor]), qubit)
            cursor += 1
        for qubit in range(width - 1):
            circuit.cx(qubit, qubit + 1)
    return Statevector.from_instruction(circuit)


def expectation(width, parameters, observable):
    state = prepare_state(width, parameters)
    return float(np.real(state.expectation_value(observable)))


def shifted_gradient(width, parameters, observable, parameter_index=0):
    plus = parameters.copy()
    minus = parameters.copy()
    plus[parameter_index] += parameter_shift
    minus[parameter_index] -= parameter_shift
    return 0.5 * (
        expectation(width, plus, observable) - expectation(width, minus, observable)
    )


rng = np.random.default_rng(307)
statistics = {}
for width in (2, 4, 6):
    local_observable = SparsePauliOp("I" * (width - 1) + "Z")
    global_observable = SparsePauliOp("Z" * width)
    local_gradients = []
    global_gradients = []
    for _ in range(sample_count):
        parameters = rng.uniform(0.0, 2.0 * np.pi, 2 * layer_count * width)
        local_gradients.append(shifted_gradient(width, parameters, local_observable))
        global_gradients.append(shifted_gradient(width, parameters, global_observable))
    statistics[width] = {
        "local_mean": float(np.mean(local_gradients)),
        "local_variance": float(np.var(local_gradients, ddof=1)),
        "global_mean": float(np.mean(global_gradients)),
        "global_variance": float(np.var(global_gradients, ddof=1)),
    }

assert all(record["local_variance"] >= 0.0 for record in statistics.values())
assert all(record["global_variance"] >= 0.0 for record in statistics.values())
assert all(np.isfinite(list(record.values())).all() for record in statistics.values())

print("ansatz=three layers of Ry, Rz, and nearest-neighbor CX gates")
print(f"sample_count_per_width={sample_count}")
print("gradient=parameter shift of the first Ry parameter")
for width, record in statistics.items():
    print(f"width={width} statistics={record}")
print("interpretation=bounded empirical diagnostic, not a universal barren-plateau proof")
