"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.4 Reading Quantum Equations: Operators and Composition
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_09_reading_quantum_equations_operators_and.py
"""

# Code: H @ ket_0     Math: H|0⟩ = |+⟩
print(f"H|0⟩ = {np.round(H @ ket_0, 4)}")   # [0.7071, 0.7071]

# Code: X @ ket_0     Math: X|0⟩ = |1⟩
print(f"X|0⟩ = {np.round(X @ ket_0, 4)}")   # [0, 1]

# Composing gates: read right to left (same as matrix multiplication)
# HX|0⟩ means "apply X first, then H"
print(f"HX|0⟩ = {np.round(H @ X @ ket_0, 4)}")  # [0.7071, -0.7071] = |−⟩
