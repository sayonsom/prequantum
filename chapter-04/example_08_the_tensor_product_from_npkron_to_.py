"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.3 The Tensor Product: From np.kron() to ⊗
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_08_the_tensor_product_from_npkron_to_.py
"""

# Fill in: bell_phi_plus = (np.kron(____, ____) + np.kron(____, ____)) / np.sqrt(2)
bell_phi_plus = (np.kron(ket_0, ket_0) + np.kron(ket_1, ket_1)) / np.sqrt(2)
print(f"|Φ+⟩ = {np.round(bell_phi_plus, 4)}")
# [0.7071, 0, 0, 0.7071]

# This CANNOT be written as |a⟩ ⊗ |b⟩ for any single-qubit states |a⟩, |b⟩
# That's the definition of entanglement: a state that won't factor.
