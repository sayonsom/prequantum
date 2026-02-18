"""
Pre Quantum - Chapter 11: Grovers Search
Code Example: Beat 3: The Concept Build > 3.8 Oracle Complexity: The Real Cost
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-11/example_11_oracle_complexity_the_real_cost.py
"""

import numpy as np

# Gate count scaling comparison
print(f"{'n':>3}  {'N':>10}  {'Classical':>12}  {'Grover':>12}  {'Speedup':>8}")
for n in [10, 20, 30, 40, 50, 64, 80, 128]:
    N = 2**n
    classical = N // 2
    grover = int(np.pi/4 * np.sqrt(N))
    speedup = classical / grover if grover > 0 else float('inf')
    print(f"  {n:3d}  {N:10.2e}  {classical:12.2e}  {grover:12.2e}  {speedup:8.1f}x")

print("\n--- Cryptographic implications ---")
print("AES-128: classical brute force = 2^127 ops")
print(f"         Grover = 2^64 ops = {2**64:.2e} oracle calls")
print("         Still enormous, but theoretically feasible")
print("\nAES-256: classical brute force = 2^255 ops")
print(f"         Grover = 2^128 ops = {2**128:.2e} oracle calls")
print("         Remains intractable even for quantum computers")
