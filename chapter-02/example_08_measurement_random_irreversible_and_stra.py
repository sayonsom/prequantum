"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.2 Measurement: Random, Irreversible, and Strange
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_08_measurement_random_irreversible_and_stra.py
"""

rng = np.random.default_rng(42)
results = []
for _ in range(10000):
    q = Qubit([1, 2])  # Biased -- amplitude for 1 is larger
    results.append(q.measure(rng))

counts = Counter(results)
print(f"0: {counts[0]}  |  1: {counts[1]}")
# 0: 1990  |  1: 8010
