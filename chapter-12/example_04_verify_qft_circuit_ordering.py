import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def qft_matrix(width):
    size = 2**width
    omega = np.exp(2j * np.pi / size)
    return np.array(
        [[omega ** (row * column) / np.sqrt(size) for column in range(size)]
         for row in range(size)],
        dtype=complex,
    )


def build_qft(width, include_final_swaps=True):
    circuit = QuantumCircuit(width, name=f"QFT-{width}")
    for target in reversed(range(width)):
        circuit.h(target)
        for control in reversed(range(target)):
            distance = target - control
            circuit.cp(np.pi / 2**distance, control, target)
    if include_final_swaps:
        for left in range(width // 2):
            circuit.swap(left, width - 1 - left)
    return circuit


def reverse_bits(value, width):
    return int(format(value, f"0{width}b")[::-1], 2)


width = 4
size = 2**width
expected = qft_matrix(width)
with_swaps = Operator(build_qft(width, include_final_swaps=True)).data
without_swaps = Operator(build_qft(width, include_final_swaps=False)).data

bit_reversal = np.zeros((size, size), dtype=complex)
for value in range(size):
    bit_reversal[reverse_bits(value, width), value] = 1.0

assert np.allclose(with_swaps, expected)
assert np.allclose(without_swaps, bit_reversal @ expected)

counts = build_qft(width).count_ops()
assert counts["h"] == width
assert counts["cp"] == width * (width - 1) // 2
assert counts["swap"] == width // 2

print(f"logical_gate_counts={dict(counts)}")
print("with_final_swaps_matches_matrix=True")
print("without_final_swaps_is_bit_reversed=True")
print("cost_boundary=logical QFT gates are not compiled hardware gates or FFT runtime")
