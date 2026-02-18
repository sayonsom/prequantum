"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.1 Classical Bits and Quantum States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_05_classical_bits_and_quantum_states.py
"""

# The amplitudes
print(f"Amplitude for 0: {q_super.state[0]}")   # 0.707...
print(f"Amplitude for 1: {q_super.state[1]}")   # 0.707...

# The probabilities (amplitude squared)
print(f"Probability of 0: {abs(q_super.state[0])**2:.4f}")  # 0.5000
print(f"Probability of 1: {abs(q_super.state[1])**2:.4f}")  # 0.5000

# They must sum to 1
total = abs(q_super.state[0])**2 + abs(q_super.state[1])**2
print(f"Total probability: {total:.4f}")  # 1.0000
