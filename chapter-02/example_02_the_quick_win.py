"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_02_the_quick_win.py
"""

# Apply a gate (matrix multiplication), THEN measure
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # The Hadamard gate

state = np.array([1, 0])        # Start in state "definitely 0"
state = H @ state                # Apply Hadamard: now in superposition
state = H @ state                # Apply Hadamard AGAIN

rng2 = np.random.default_rng(42)
results = rng2.choice([0, 1], size=10000, p=[abs(state[0])**2, abs(state[1])**2])
counts = Counter(results)

print(f"After H applied twice:")
print(f"0: {counts[0]} times ({counts[0]/100:.1f}%)")
print(f"1: {counts[1]} times ({counts[1]/100:.1f}%)")
# After H applied twice:
# 0: 10000 times (100.0%)
# 1: 0 times (0.0%)
