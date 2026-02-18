"""
Pre Quantum - Chapter 04: The Math You Already Know
Code Example: Beat 3: The Concept Build > 3.4 Reading Quantum Equations: Operators and Composition
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-04/example_10_reading_quantum_equations_operators_and.py
"""

# Math: |Φ+⟩ = CNOT · (H ⊗ I) |00⟩
step0 = np.kron(ket_0, ket_0)              # |00⟩
step1 = np.kron(H, I) @ step0              # (H⊗I)|00⟩ = (|00⟩+|10⟩)/√2
step2 = CNOT @ step1                       # CNOT → (|00⟩+|11⟩)/√2

print(f"|00⟩            = {np.round(step0, 4)}")
print(f"(H⊗I)|00⟩      = {np.round(step1, 4)}")
print(f"CNOT·(H⊗I)|00⟩ = {np.round(step2, 4)}")
