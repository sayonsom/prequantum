"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.3 The Tensor Product: From np.kron() to ⊗
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_07_the_tensor_product_from_npkron_to_.py
"""

# |+⟩ ⊗ |0⟩ -- first qubit in superposition, second definite
result = np.kron(ket_plus, ket_0)
print(f"|+⟩ ⊗ |0⟩ = {np.round(result, 4)}")
# [0.7071, 0, 0.7071, 0] → amplitudes at |00⟩ and |10⟩

# The tensor product distributes over addition (like multiplication):
#   (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2
# This is SEPARABLE -- you can factor it back into individual qubits
