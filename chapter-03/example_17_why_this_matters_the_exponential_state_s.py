"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.7 Why This Matters: The Exponential State Space
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_17_why_this_matters_the_exponential_state_s.py
"""

# 3 qubits: build and explore
q = np.array([1, 0], dtype=complex)
system_3 = np.kron(np.kron(q, q), q)
print(f"3 qubits: {len(system_3)} amplitudes")

for i in range(8):
    label = format(i, '03b')
    print(f"  Index {i} -> outcome '{label}'")
