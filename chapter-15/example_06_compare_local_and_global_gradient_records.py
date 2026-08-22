"""Compare local and global gradient variance in one declared circuit family."""

import numpy as np


def ry(angle):
    return np.array([
        [np.cos(angle / 2), -np.sin(angle / 2)],
        [np.sin(angle / 2), np.cos(angle / 2)],
    ], dtype=complex)


def rz(angle):
    return np.diag([np.exp(-0.5j * angle), np.exp(0.5j * angle)])


def apply_one_qubit(state, gate, qubit, qubits):
    tensor = state.reshape([2] * qubits)
    tensor = np.moveaxis(tensor, qubit, 0)
    tensor = (gate @ tensor.reshape(2, -1)).reshape([2] + [2] * (qubits - 1))
    return np.moveaxis(tensor, 0, qubit).reshape(-1)


def apply_cz(state, left, right, qubits):
    result = state.copy()
    indices = np.arange(state.size)
    left_bits = (indices >> (qubits - 1 - left)) & 1
    right_bits = (indices >> (qubits - 1 - right)) & 1
    result[(left_bits & right_bits).astype(bool)] *= -1
    return result


def circuit_state(parameters, qubits):
    layers = parameters.shape[0]
    state = np.zeros(2**qubits, dtype=complex)
    state[0] = 1.0
    for layer in range(layers):
        for qubit in range(qubits):
            state = apply_one_qubit(
                state, ry(parameters[layer, qubit, 0]), qubit, qubits
            )
            state = apply_one_qubit(
                state, rz(parameters[layer, qubit, 1]), qubit, qubits
            )
        for qubit in range(qubits - 1):
            state = apply_cz(state, qubit, qubit + 1, qubits)
        if qubits > 2:
            state = apply_cz(state, qubits - 1, 0, qubits)
    return state


def costs(parameters, qubits):
    probabilities = abs(circuit_state(parameters, qubits)) ** 2
    indices = np.arange(probabilities.size)
    z_first = np.where(((indices >> (qubits - 1)) & 1) == 0, 1.0, -1.0)
    local_cost = float(probabilities @ z_first)
    global_cost = float(probabilities[0])
    return local_cost, global_cost


def shifted_gradient(parameters, qubits, cost_index):
    plus = parameters.copy()
    minus = parameters.copy()
    plus[0, 0, 0] += np.pi / 2
    minus[0, 0, 0] -= np.pi / 2
    return 0.5 * (
        costs(plus, qubits)[cost_index] - costs(minus, qubits)[cost_index]
    )


rng = np.random.default_rng(5)
layers = 4
samples = 128
print("qubits local_gradient_variance global_gradient_variance")
for qubits in [2, 4, 6, 8]:
    local_gradients = []
    global_gradients = []
    for _ in range(samples):
        parameters = rng.uniform(-np.pi, np.pi, size=(layers, qubits, 2))
        local_gradients.append(shifted_gradient(parameters, qubits, 0))
        global_gradients.append(shifted_gradient(parameters, qubits, 1))
    local_variance = float(np.var(local_gradients))
    global_variance = float(np.var(global_gradients))
    print(f"{qubits:>6} {local_variance:>23.6e} {global_variance:>24.6e}")

print("boundary=this finite exact simulation diagnoses one ansatz and two costs; "
      "it is not a universal scaling proof")
