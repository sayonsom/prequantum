"""
Pre Quantum - Chapter 10: Your First Quantum Algorithms
Code Example: Beat 3: The Concept Build > 3.5 The Bernstein-Vazirani Algorithm
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-10/example_08_the_bernstein_vazirani_algorithm.py
"""

import numpy as np

# Classical BV: n queries, one bit per query
def classical_bv(secret, n):
    """Classically find s by querying f(e_i) for each unit vector."""
    queries = 0
    found = []
    for i in range(n):
        # Query f(e_i) where e_i has a 1 only in position i
        e_i = [0] * n
        e_i[i] = 1
        # f(e_i) = s · e_i = s_i (just the i-th bit of s)
        s_dot_ei = sum(int(secret[j]) * e_i[j] for j in range(n)) % 2
        found.append(str(s_dot_ei))
        queries += 1
    return ''.join(found), queries

# Test
secret = "10110011"
classical_result, classical_queries = classical_bv(secret, len(secret))
print(f"Secret: {secret}")
print(f"Classical: found {classical_result} in {classical_queries} queries")
print(f"Quantum:   found {secret} in 1 query")
print(f"Speedup:   {classical_queries}x fewer oracle calls")
