"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.7 Query Complexity: Making "Faster" Precise
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_10_query_complexity_making_faster_precise.py
"""

import numpy as np

# Comparing query complexity: classical vs quantum

algorithms = {
    "Deutsch-Jozsa": {
        "classical_worst": lambda n: 2**(n-1) + 1,
        "classical_best": lambda n: 2,
        "quantum": lambda n: 1,
    },
    "Bernstein-Vazirani": {
        "classical_worst": lambda n: n,
        "classical_best": lambda n: n,
        "quantum": lambda n: 1,
    },
    "Grover (Ch. 11)": {
        "classical_worst": lambda n: 2**n,
        "classical_best": lambda n: 1,
        "quantum": lambda n: int(np.ceil(np.pi/4 * np.sqrt(2**n))),
    },
}

print(f"{'Algorithm':<25} {'n':>4} {'Classical worst':>16} {'Quantum':>10} {'Speedup':>12}")
print("-" * 70)
for name, costs in algorithms.items():
    for n_val in [4, 10, 20]:
        cw = costs["classical_worst"](n_val)
        q = costs["quantum"](n_val)
        speedup = f"{cw/q:.0f}x"
        print(f"{name:<25} {n_val:>4} {cw:>16,} {q:>10} {speedup:>12}")
    print()
