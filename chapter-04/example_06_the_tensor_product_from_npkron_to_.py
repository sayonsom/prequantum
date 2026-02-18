"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.3 The Tensor Product: From np.kron() to ⊗
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_06_the_tensor_product_from_npkron_to_.py
"""

# |0⟩ ⊗ |1⟩ = |01⟩
result = np.kron(ket_0, ket_1)
print(f"|0⟩ ⊗ |1⟩ = {result}")
# [0, 1, 0, 0] → index 1 has amplitude 1, meaning "01"

# How kron works: every product of amplitudes
manual = np.array([
    ket_0[0]*ket_1[0],  # 1*0 = 0  (|00⟩)
    ket_0[0]*ket_1[1],  # 1*1 = 1  (|01⟩) ← this one
    ket_0[1]*ket_1[0],  # 0*0 = 0  (|10⟩)
    ket_0[1]*ket_1[1],  # 0*1 = 0  (|11⟩)
], dtype=complex)
print(f"Match: {np.allclose(result, manual)}")  # True
