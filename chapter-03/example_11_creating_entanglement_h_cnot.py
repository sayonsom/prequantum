"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.4 Creating Entanglement: H + CNOT
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_11_creating_entanglement_h_cnot.py
"""

# We need: kron([a,b], [c,d]) = [a*c, a*d, b*c, b*d] = [0.7071, 0, 0, 0.7071]
#
# From index 1: a*d = 0  -> either a=0 or d=0
# From index 0: a*c = 0.7071  -> a != 0
# Therefore: d = 0
# From index 3: b*d = 0.7071  -> but d=0 -> 0 != 0.7071
#
# CONTRADICTION.

print("Can we factor [0.7071, 0, 0, 0.7071] into kron(q0, q1)?")
print("No. The system of equations has no solution.")
print("This state is ENTANGLED.")
