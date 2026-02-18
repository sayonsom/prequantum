"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.4 Reading Quantum Equations: Operators and Composition
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_11_reading_quantum_equations_operators_and.py
"""

# U @ U† = I  (the † symbol means conjugate transpose)
print(f"H @ H† = I? {np.allclose(H @ H.conj().T, np.eye(2))}")  # True
print(f"X @ X† = I? {np.allclose(X @ X.conj().T, np.eye(2))}")  # True
