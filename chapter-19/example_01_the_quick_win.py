"""
Pre Quantum - Chapter 19: Quantum Cryptography
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-19/example_01_the_quick_win.py
"""

import numpy as np
from math import gcd

def shors_classical_simulation(N, a=None):
    """Simulate Shor's algorithm classically: find factors of N.

    The quantum part is Step 2: period-finding via QPE + QFT.
    Classically, we brute-force the period. A quantum computer
    uses O(n^3) gates where n = number of bits in N.
    """
    if N % 2 == 0:
        return 2, N // 2

    # Step 1: Pick random a < N (or use provided)
    if a is None:
        np.random.seed(42)
        a = np.random.randint(2, N)

    # Check if we got lucky -- gcd(a, N) > 1
    g = gcd(a, N)
    if g > 1:
        return g, N // g

    # Step 2: Find the period r of f(x) = a^x mod N
    # This is the step a quantum computer does exponentially faster.
    # Classical: iterate through all r up to N (worst case exponential).
    # Quantum: QPE finds r in O(n^3) gates via the QFT.
    r = 1
    while pow(a, r, N) != 1:
        r += 1
        if r > N:
            return None, None  # failed

    # Step 3: If r is even, try gcd(a^(r/2) ± 1, N)
    # Mathematical basis: if a^r ≡ 1 (mod N) and r is even, then
    # a^(r/2) is a square root of 1 mod N. Since N = pq, there are
    # four square roots of 1 mod N (by CRT), and with probability ≥ 1/2,
    # a^(r/2) is a non-trivial one, yielding factors via gcd.
    if r % 2 != 0:
        return None, None  # need even period

    half = pow(a, r // 2, N)
    factor1 = gcd(half - 1, N)
    factor2 = gcd(half + 1, N)

    if factor1 != 1 and factor1 != N:
        return factor1, N // factor1
    if factor2 != 1 and factor2 != N:
        return factor2, N // factor2
    return None, None

# Factor some numbers
test_cases = [15, 21, 35, 77, 91, 143, 221, 323]
print(f"{'N':>6}  {'a':>3}  {'r':>3}  {'Factors':>12}  {'Verify':>8}")
print("-" * 40)
for N in test_cases:
    # Try a few values of a
    for a in range(2, N):
        g = gcd(a, N)
        if g > 1:
            p, q = g, N // g
            print(f"{N:>6}  {a:>3}  {'gcd':>3}  {p:>5} × {q:<5}  {p*q == N}")
            break
        r = 1
        while pow(a, r, N) != 1 and r <= N:
            r += 1
        if r <= N and r % 2 == 0:
            half = pow(a, r // 2, N)
            f1, f2 = gcd(half - 1, N), gcd(half + 1, N)
            if f1 not in (1, N):
                print(f"{N:>6}  {a:>3}  {r:>3}  {f1:>5} × {N//f1:<5}  {f1*(N//f1)==N}")
                break
            if f2 not in (1, N):
                print(f"{N:>6}  {a:>3}  {r:>3}  {f2:>5} × {N//f2:<5}  {f2*(N//f2)==N}")
                break

# Updated resource estimates (Gidney 2025, Pinnacle 2026)
print(f"\n--- Why this matters: Updated Resource Estimates ---")
print(f"RSA-2048: N has ~617 digits")
print(f"Classical factoring: ~2^110 operations (~billions of years)")
print(f"Shor's algorithm:    O(n^3) = ~2048^3 ≈ 8.6B gates (minutes on fault-tolerant QC)")
print(f"")
print(f"{'Year':<6} {'Physical Qubits':>18} {'Runtime':>12} {'Source'}")
print(f"{'-'*55}")
print(f"{'2019':<6} {'~20 million':>18} {'~8 hours':>12} Gidney & Ekerå")
print(f"{'2025':<6} {'< 1 million':>18} {'~1 week':>12} Gidney (Google)")
print(f"{'2026':<6} {'< 100,000':>18} {'TBD':>12} Pinnacle (QLDPC codes)")
print(f"")
print(f"The bar is dropping fast. Three innovations drove the 20x reduction:")
print(f"  1. Approximate residue arithmetic (fewer gates)")
print(f"  2. Yoked surface codes (3x storage density for idle qubits)")
print(f"  3. Magic state cultivation (replaces distillation, ~100x fewer Toffolis)")
# Output:
#      N    a    r       Factors    Verify
# ----------------------------------------
#     15    2    4      3 × 5      True
#     21    2    6      7 × 3      True
#     35    2   12      7 × 5      True
#     77    2   30      7 × 11     True
#     91    2   12      7 × 13     True
#    143    2   60     11 × 13     True
#    221    2   24     13 × 17     True
#    323    2   72     19 × 17     True
#
# --- Why this matters: Updated Resource Estimates ---
# RSA-2048: N has ~617 digits
# Classical factoring: ~2^110 operations (~billions of years)
# Shor's algorithm:    O(n^3) = ~2048^3 ≈ 8.6B gates (minutes on fault-tolerant QC)
#
# Year   Physical Qubits      Runtime Source
# -------------------------------------------------------
# 2019        ~20 million     ~8 hours Gidney & Ekerå
# 2025        < 1 million      ~1 week Gidney (Google)
# 2026          < 100,000          TBD Pinnacle (QLDPC codes)
#
# The bar is dropping fast. Three innovations drove the 20x reduction:
#   1. Approximate residue arithmetic (fewer gates)
#   2. Yoked surface codes (3x storage density for idle qubits)
#   3. Magic state cultivation (replaces distillation, ~100x fewer Toffolis)
