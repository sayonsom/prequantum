"""
Pre Quantum - Chapter 09: The Math Deepens
Code Example: Beat 3: The Concept Build > 3.2 Dimension: Why 2^n Changes Everything
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-09/example_03_dimension_why_2n_changes_everything.py
"""

import numpy as np

# 1 qubit: 2D space, 2 basis vectors
n_qubits = 1
dim = 2**n_qubits
print(f"{n_qubits} qubit:  {dim}D space, {dim} basis vectors")

# 2 qubits: 4D space
n_qubits = 2
dim = 2**n_qubits
basis_labels = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
print(f"{n_qubits} qubits: {dim}D space → {basis_labels}")

# 3 qubits: 8D space
n_qubits = 3
dim = 2**n_qubits
print(f"{n_qubits} qubits: {dim}D space → {dim} basis vectors")

# The scaling problem:
for n in [10, 20, 30, 50, 100]:
    dim = 2**n
    print(f"{n} qubits: {dim:>30,}D space")

# At 50 qubits, the state vector has ~10^15 entries.
# That's why Google's Sycamore (53 qubits) was hard to simulate classically.
# And why Google's Willow (105 qubits, 2024) pushes even further.
print(f"\n50-qubit state vector: {2**50:,} complex amplitudes")
print(f"Memory needed: ~{2**50 * 16 / 1e15:.1f} petabytes (at 16 bytes each)")
