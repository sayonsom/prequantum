"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.6 From Period Finding to Factoring
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_08_from_period_finding_to_factoring.py
"""

import numpy as np
from math import gcd
from fractions import Fraction

# Classical demonstration: why period finding → factoring

N = 15

print(f"Factoring N = {N}")
print(f"{'a':>3s} {'r':>3s} {'a^(r/2)':>8s} {'gcd(a^(r/2)-1,N)':>18s} {'gcd(a^(r/2)+1,N)':>18s} {'factors':>10s}")
print("-" * 70)

for a in range(2, N):
    if gcd(a, N) != 1:
        print(f"{a:3d}  --  gcd({a},{N})={gcd(a,N)} → trivial factor!")
        continue

    # Find period: smallest r > 0 with a^r ≡ 1 (mod N)
    r = 1
    while pow(a, r, N) != 1:
        r += 1

    if r % 2 != 0:
        print(f"{a:3d} {r:3d}  odd period, skip")
        continue

    half = pow(a, r // 2, N)
    f1 = gcd(half - 1, N)
    f2 = gcd(half + 1, N)

    if f1 == 1 or f1 == N:
        print(f"{a:3d} {r:3d} {half:8d} {f1:18d} {f2:18d}  trivial")
    else:
        print(f"{a:3d} {r:3d} {half:8d} {f1:18d} {f2:18d}  → {f1} × {f2}")
