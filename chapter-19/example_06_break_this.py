"""
Pre Quantum - Chapter 19: Quantum Cryptography
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-19/example_06_break_this.py
"""

import numpy as np

rng = np.random.RandomState(42)
n = 50

alice_bits = rng.randint(0, 2, n)
alice_bases = rng.randint(0, 2, n)
bob_bases = rng.randint(0, 2, n)

# Eve intercepts and measures
eve_bases = rng.randint(0, 2, n)

# BUG: Eve re-prepares in ALICE'S basis instead of her own
bob_bits = np.zeros(n, dtype=int)
for i in range(n):
    if bob_bases[i] == alice_bases[i]:  # matching bases
        bob_bits[i] = alice_bits[i]     # Eve re-prepared in correct basis!
    else:
        bob_bits[i] = rng.randint(0, 2)

matching = alice_bases == bob_bases
errors = np.sum(alice_bits[matching] != bob_bits[matching])
print(f"Error rate: {errors}/{np.sum(matching)} = {errors/np.sum(matching):.1%}")
# Shows 0% -- Eve is invisible!
