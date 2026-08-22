import numpy as np

CNOT_01 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
], dtype=complex)
CNOT_10 = np.array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
], dtype=complex)
SWAP = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
], dtype=complex)

swap_from_cnots = CNOT_01 @ CNOT_10 @ CNOT_01
print("three CNOTs give SWAP:", np.allclose(swap_from_cnots, SWAP))

ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)
bell = CNOT_01 @ np.kron(ket_plus, ket_0)
expected_bell = (np.kron(ket_0, ket_0) + np.kron(ket_1, ket_1)) / np.sqrt(2)
print("CNOT can create Bell Phi-plus:", np.allclose(bell, expected_bell))
print("CNOT leaves |00> unchanged:",
      np.allclose(CNOT_01 @ np.kron(ket_0, ket_0), np.kron(ket_0, ket_0)))

toffoli = np.eye(8, dtype=complex)
toffoli[[6, 6, 7, 7], [6, 7, 6, 7]] = [0, 1, 1, 0]
for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
    input_index = int(f"{a}{b}0", 2)
    output_index = np.argmax(np.abs(toffoli[:, input_index]))
    print(f"{a}{b}0 -> {output_index:03b}")

# three CNOTs give SWAP: True
# CNOT can create Bell Phi-plus: True
# CNOT leaves |00> unchanged: True
# 000 -> 000
# 010 -> 010
# 100 -> 100
# 110 -> 111
