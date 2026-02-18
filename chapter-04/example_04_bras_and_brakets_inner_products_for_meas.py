"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.2 Bras and Brakets: Inner Products for Measurement
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_04_bras_and_brakets_inner_products_for_meas.py
"""

# Bra = conjugate transpose. For real-valued states, identical to the ket.
bra_0 = ket_0.conj()   # ⟨0|
bra_1 = ket_1.conj()   # ⟨1|

# Where conjugate matters: complex amplitudes
ket_complex = np.array([1+2j, 3-1j], dtype=complex) / np.sqrt(15)
bra_complex = ket_complex.conj()
print(f"|ψ⟩ = {np.round(ket_complex, 4)}")
print(f"⟨ψ| = {np.round(bra_complex, 4)}")
# Notice: 1+2j becomes 1-2j, 3-1j becomes 3+1j

# Braket: the inner product
print(f"\n⟨0|0⟩ = {braket(ket_0, ket_0)}")        # 1 -- full overlap
print(f"⟨0|1⟩ = {braket(ket_0, ket_1)}")           # 0 -- orthogonal
print(f"⟨+|−⟩ = {braket(ket_plus, ket_minus)}")    # 0 -- also orthogonal!

# Measurement probabilities via Born rule
print(f"\n⟨0|+⟩ = {braket(ket_0, ket_plus):.4f}")
print(f"|⟨0|+⟩|² = {abs(braket(ket_0, ket_plus))**2:.4f}")  # 0.5
print(f"|⟨1|+⟩|² = {abs(braket(ket_1, ket_plus))**2:.4f}")  # 0.5
print(f"Sum = {abs(braket(ket_0, ket_plus))**2 + abs(braket(ket_1, ket_plus))**2}")  # 1.0
