"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_10_break_this.py
"""

import numpy as np

# Select exactly 2 out of 4 items
n = 4
budget = 2
penalty = 10

Q = np.zeros((n, n))
# Costs on diagonal
costs = [3, 5, 2, 7]
for i in range(n):
    Q[i, i] = costs[i]

# Penalty: λ(Σx_i - 2)²
# BUG: missing the cross terms!
for i in range(n):
    Q[i, i] += penalty * (1 - 2 * budget)  # linear part only

# Missing: Q[i,j] += penalty * 2 for all i < j

print("QUBO matrix (buggy):")
print(Q)

# Test: x = [1, 0, 1, 0] should be feasible (sum = 2)
x = np.array([1, 0, 1, 0])
print(f"\nf([1,0,1,0]) = {x @ Q @ x:.0f}")
print("Expected: 3 + 2 = 5 (just costs, zero penalty)")
print("But we get something wrong because the QUBO is incomplete!")
