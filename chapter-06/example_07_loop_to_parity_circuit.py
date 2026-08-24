"""Turn a Python construction loop into a reversible parity circuit."""

from itertools import product

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def make_parity_block(data_width: int) -> QuantumCircuit:
    """Return a reusable block whose last qubit accumulates XOR parity."""
    block = QuantumCircuit(data_width + 1, name="PARITY")
    accumulator = data_width
    for source in range(data_width):
        block.cx(source, accumulator)
    return block


data_width = 3
parity_block = make_parity_block(data_width)

for bits in product([0, 1], repeat=data_width):
    program = QuantumCircuit(data_width + 1)
    for qubit, bit in enumerate(bits):
        if bit:
            program.x(qubit)
    program.compose(parity_block, inplace=True)

    probabilities = Statevector.from_instruction(program).probabilities_dict()
    observed_label = max(probabilities, key=probabilities.get)
    observed_accumulator = int(observed_label[0])
    expected_accumulator = sum(bits) % 2

    assert observed_accumulator == expected_accumulator

print("controlled-X operations:", parity_block.count_ops()["cx"])
print("verified basis inputs:", 2**data_width)
