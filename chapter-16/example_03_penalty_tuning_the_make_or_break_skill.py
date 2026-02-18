"""
Pre Quantum - Chapter 16: Quantum Optimization
Code Example: Beat 3: The Concept Build > 3.2 Penalty Tuning: The Make-or-Break Skill
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-16/example_03_penalty_tuning_the_make_or_break_skill.py
"""

import numpy as np
from itertools import product

def evaluate_penalty_sensitivity(generators, demand, penalties):
    """Show how penalty weight affects which solution the QUBO picks."""
    n = len(generators)

    print(f"{'Penalty':<10} {'Best Config':<15} {'Power':>7} {'Cost':>7} {'Feasible':>10} {'Gap to 2nd':>12}")
    print("-" * 65)

    for pen in penalties:
        Q = np.zeros((n, n))
        for i in range(n):
            p_i, c_i = generators[i]
            Q[i, i] = c_i + pen * (p_i**2 - 2 * demand * p_i)
        for i in range(n):
            for j in range(i+1, n):
                Q[i, j] = pen * 2 * generators[i][0] * generators[j][0]
        qubo_offset = pen * demand**2

        results = []
        for bits in product([0, 1], repeat=n):
            x = np.array(bits)
            val = x @ Q @ x + qubo_offset
            power = sum(g[0]*b for g, b in zip(generators, bits))
            cost = sum(g[1]*b for g, b in zip(generators, bits))
            feasible = (power == demand)
            results.append((val, bits, power, cost, feasible))

        results.sort(key=lambda r: r[0])
        best = results[0]
        second = results[1]
        gap = second[0] - best[0]

        feas_str = "YES" if best[4] else "NO!"
        print(f"  {pen:<8} {str(best[1]):<15} {best[2]:>5} MW  ${best[3]:>5}  {feas_str:>10}  {gap:>10.0f}")

generators = [(50, 30), (80, 45), (100, 60)]
demand = 150

# Try penalty weights from way too small to way too large
evaluate_penalty_sensitivity(generators, demand,
                              [0.01, 0.1, 0.5, 1, 5, 10, 50, 100])
# Output:
# Penalty    Best Config     Power    Cost   Feasible    Gap to 2nd
# -----------------------------------------------------------------
#   0.01     (1, 1, 1)        230 MW   $135         NO!          -1
#   0.1      (1, 1, 1)        230 MW   $135         NO!         -61
#   0.5      (0, 1, 1)        180 MW   $105         NO!        -204
#   1        (1, 0, 1)        150 MW    $90        YES          426
#   5        (1, 0, 1)        150 MW    $90        YES         3780
#   10       (1, 0, 1)        150 MW    $90        YES         7560
#   50       (1, 0, 1)        150 MW    $90        YES        37800
#   100      (1, 0, 1)        150 MW    $90        YES        75600
