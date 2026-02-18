"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.2 Bras and Brakets: Inner Products for Measurement
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_05_bras_and_brakets_inner_products_for_meas.py
"""

# Both {|0⟩, |1⟩} and {|+⟩, |−⟩} are orthonormal bases
# Orthonormal = mutually orthogonal + self-overlap = 1
for name, basis in [("Computational", [ket_0, ket_1]), ("Hadamard", [ket_plus, ket_minus])]:
    cross = braket(basis[0], basis[1])
    self0 = braket(basis[0], basis[0])
    self1 = braket(basis[1], basis[1])
    print(f"{name}: self={self0:.0f},{self1:.0f}  cross={cross:.0f}")
