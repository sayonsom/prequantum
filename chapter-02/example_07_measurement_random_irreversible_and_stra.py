"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.2 Measurement: Random, Irreversible, and Strange
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_07_measurement_random_irreversible_and_stra.py
"""

from collections import Counter

rng = np.random.default_rng(42)
results = []
for _ in range(10000):
    q = Qubit([1, 1])  # Fresh superposition each time
    results.append(q.measure(rng))

counts = Counter(results)
print(f"0: {counts[0]}  |  1: {counts[1]}")
# 0: 4976  |  1: 5024
