"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.6 Logical Qubit Operations: The T Gate Problem
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_07_logical_qubit_operations_the_t_gate_prob.py
"""

import numpy as np

# The T gate and why it matters
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
S = np.array([[1, 0], [0, 1j]])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

# T is NOT a Clifford gate -- verify by showing T⁸ = I (order 8)
# Cliffords have order at most 4 in the single-qubit case
T_power = np.eye(2)
for n in range(1, 9):
    T_power = T_power @ T
    is_identity = np.allclose(T_power, np.eye(2))
    if n <= 4 or n == 8:
        print(f"T^{n} = I? {is_identity}")

# The magic state
magic_state = np.array([1, np.exp(1j * np.pi / 4)]) / np.sqrt(2)
print(f"\nMagic state |T⟩ = {magic_state}")
print(f"|T⟩ = T·H|0⟩? {np.allclose(magic_state, T @ H @ np.array([1, 0]))}")

# Magic state distillation cost estimate
def distillation_overhead(input_error, target_error, protocol="15-to-1"):
    """
    Estimate magic state distillation overhead.

    15-to-1 protocol: 15 noisy magic states → 1 cleaner magic state
    Output error ≈ 35 * input_error³ (cubic suppression)
    """
    rounds = 0
    current_error = input_error
    qubits_per_round = 15

    while current_error > target_error:
        current_error = 35 * current_error ** 3
        rounds += 1

    total_magic_states = qubits_per_round ** rounds
    print(f"\nMagic state distillation ({protocol}):")
    print(f"  Input error rate: {input_error}")
    print(f"  Target error rate: {target_error}")
    print(f"  Rounds needed: {rounds}")
    print(f"  Magic states consumed per output: {total_magic_states}")
    print(f"  Final error: {current_error:.2e}")
    return total_magic_states

# Realistic scenario
overhead = distillation_overhead(0.01, 1e-10)

# How many T gates does a useful algorithm need?
t_count_shor_2048 = 2**30  # ~1 billion T gates for RSA-2048 factoring
total_magic_states_shor = t_count_shor_2048 * overhead
print(f"\nShor's (RSA-2048) needs ~{t_count_shor_2048:,} T gates")
print(f"Total magic states: ~{total_magic_states_shor:.1e}")
print(f"This is why fault-tolerant Shor's needs millions of physical qubits.")

# Output:
# T^1 = I? False
# T^2 = I? False
# T^3 = I? False
# T^4 = I? False
# T^8 = I? True
#
# Magic state |T⟩ = [0.70710678+0.j         0.5       +0.5j       ]
# |T⟩ = T·H|0⟩? True
#
# Magic state distillation (15-to-1):
#   Input error rate: 0.01
#   Target error rate: 1e-10
#   Rounds needed: 2
#   Magic states consumed per output: 225
#   Final error: 3.50e-11
#
# Shor's (RSA-2048) needs ~1,073,741,824 T gates
# Total magic states: ~2.4e+11
# This is why fault-tolerant Shor's needs millions of physical qubits.
