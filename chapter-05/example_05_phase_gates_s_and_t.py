"""
Pre Quantum - Chapter 05: Quantum Gates as Transformations
Code Example: Beat 3: The Concept Build > 3.2 Phase Gates: S and T
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-05/example_05_phase_gates_s_and_t.py
"""

import numpy as np

# The phase gate family
# Z adds phase π (180°) to |1⟩
Z = np.array([[1, 0], [0, np.exp(1j * np.pi)]], dtype=complex)  # = [[1,0],[0,-1]]

# S adds phase π/2 (90°) to |1⟩
S = np.array([[1, 0], [0, np.exp(1j * np.pi / 2)]], dtype=complex)  # = [[1,0],[0,i]]

# T adds phase π/4 (45°) to |1⟩
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

print("Phase gates on |1⟩:")
ket_1 = np.array([0, 1], dtype=complex)
print(f"  Z|1⟩ = {np.round(Z @ ket_1, 4)}")  # [0, -1]     → phase = π
print(f"  S|1⟩ = {np.round(S @ ket_1, 4)}")  # [0,  i]     → phase = π/2
print(f"  T|1⟩ = {np.round(T @ ket_1, 4)}")  # [0, 0.707+0.707i] → phase = π/4

# The hierarchy: T² = S, S² = Z
print(f"\nT² = S? {np.allclose(T @ T, S)}")  # True
print(f"S² = Z? {np.allclose(S @ S, Z)}")    # True
# So T is the "square root" of S, and S is the "square root" of Z
