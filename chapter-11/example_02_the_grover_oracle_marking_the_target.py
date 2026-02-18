"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.1 The Grover Oracle: Marking the Target
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_02_the_grover_oracle_marking_the_target.py
"""

import numpy as np

N = 8  # 2³ = 8 items
n = 3  # 3 qubits

# Target state: |5⟩ = |101⟩
target_idx = 5
target_state = np.zeros(N, dtype=complex)
target_state[target_idx] = 1.0

# Oracle matrix: I - 2|w⟩⟨w|
I = np.eye(N, dtype=complex)
oracle = I - 2 * np.outer(target_state, target_state.conj())

# Verify: oracle flips only the target
for i in range(N):
    basis = np.zeros(N, dtype=complex)
    basis[i] = 1.0
    result = oracle @ basis
    phase = result[i].real
    label = f"|{format(i, f'0{n}b')}⟩"
    print(f"  O{label} = {'+' if phase > 0 else ''}{phase:.0f}{label}"
          f"{'  ← TARGET (phase flipped!)' if i == target_idx else ''}")
