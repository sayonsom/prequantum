"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.4 Creating Entanglement: H + CNOT
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_13_creating_entanglement_h_cnot.py
"""

def is_separable(state):
    """Quick test: is a 2-qubit state separable?"""
    return np.isclose(state[0] * state[3], state[1] * state[2])

bell = np.array([0.7071, 0, 0, 0.7071], dtype=complex)
indep = np.array([0.5, 0.5, 0.5, 0.5], dtype=complex)

print(f"Bell state separable? {is_separable(bell)}")    # False
print(f"Independent separable? {is_separable(indep)}")  # True
