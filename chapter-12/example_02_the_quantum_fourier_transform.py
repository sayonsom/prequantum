"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.1 The Quantum Fourier Transform
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_02_the_quantum_fourier_transform.py
"""

import numpy as np

# Build the QFT matrix for N=8 (3 qubits)
N = 8
omega = np.exp(2j * np.pi / N)  # primitive Nth root of unity

# QFT matrix: (QFT)_{jk} = ω^(jk) / √N
QFT_matrix = np.array([[omega**(j*k) / np.sqrt(N) for k in range(N)]
                        for j in range(N)])

print("QFT matrix (N=8), real parts:")
print(np.round(QFT_matrix.real, 3))
print("\nQFT matrix (N=8), imaginary parts:")
print(np.round(QFT_matrix.imag, 3))

# Key property: QFT is UNITARY
print(f"\nQFT†·QFT = I? {np.allclose(QFT_matrix.conj().T @ QFT_matrix, np.eye(N))}")

# Verify the product representation for |j=5⟩ = |101⟩
j = 5  # binary: 101 → j1=1, j2=0, j3=1
j_bits = [1, 0, 1]  # MSB first

# Product form: each qubit k gets phase from bits j_{n-k+1} ... j_n
# Qubit 0 (MSB of output): phase = 0.j3 = 0.1 = 1/2
# Qubit 1: phase = 0.j2j3 = 0.01 = 1/4
# Qubit 2 (LSB of output): phase = 0.j1j2j3 = 0.101 = 5/8
phases_product = [
    1/2,    # 0.j3 = 0.1
    1/4,    # 0.j2j3 = 0.01
    5/8     # 0.j1j2j3 = 0.101
]

# Build the state from the product form
product_state = np.ones(1, dtype=complex)
for phase in phases_product:
    qubit = np.array([1, np.exp(2j * np.pi * phase)]) / np.sqrt(2)
    product_state = np.kron(product_state, qubit)

# Compare with direct QFT application
basis_5 = np.zeros(N, dtype=complex)
basis_5[5] = 1.0
direct_state = QFT_matrix @ basis_5

print(f"\nQFT|101⟩ via product form matches direct? "
      f"{np.allclose(product_state, direct_state)}")

# Apply to basis states
for j in range(N):
    basis = np.zeros(N, dtype=complex)
    basis[j] = 1.0
    transformed = QFT_matrix @ basis
    phases = np.angle(transformed) / (2 * np.pi)
    print(f"\nQFT|{format(j, '03b')}⟩: amplitudes all = {abs(transformed[0]):.4f}")
    print(f"  phases: {np.round(phases * N, 1)}")
