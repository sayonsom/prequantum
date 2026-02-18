"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.4 Creating Entanglement: H + CNOT
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_10_creating_entanglement_h_cnot.py
"""

state = CNOT @ state
print(f"After CNOT:    {np.round(state, 4)}")
# [0.7071, 0, 0, 0.7071]
