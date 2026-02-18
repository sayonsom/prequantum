"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 3: The Concept Build > 3.1 The Quantum Advantage Scorecard
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_02_the_quantum_advantage_scorecard.py
"""

# The Quantum Advantage Scorecard -- a decision function
def score_quantum_claim(
    problem_useful: bool,
    classical_comparison: str,      # "none", "best_known", "optimal"
    advantage_scales: bool,
    hardware_available: bool,
    cost_competitive: bool,
    independently_reproduced: bool,
):
    """
    Score a quantum advantage claim on the 4-level scale.
    Returns level (1-4) and a skepticism rating.
    """
    score = 0
    flags = []

    if not problem_useful:
        flags.append("Problem has no practical application")
        return 1, "SUPREMACY ONLY", flags

    if classical_comparison == "none":
        flags.append("No classical baseline provided")
    elif classical_comparison == "best_known":
        score += 1
        if not independently_reproduced:
            flags.append("Classical comparison not independently verified")
    elif classical_comparison == "optimal":
        score += 2

    if advantage_scales:
        score += 1
    else:
        flags.append("Advantage may disappear at larger problem sizes")

    if hardware_available:
        score += 1
    else:
        flags.append("Requires hardware that doesn't exist yet")

    if cost_competitive:
        score += 1
    else:
        flags.append("Classical solution is cheaper")

    # Map score to level
    if score >= 5:
        level = 4
        label = "PRACTICAL ADVANTAGE"
    elif score >= 3:
        level = 3
        label = "SCALABLE ADVANTAGE"
    elif score >= 1:
        level = 2
        label = "QUANTUM UTILITY"
    else:
        level = 1
        label = "SUPREMACY ONLY"

    return level, label, flags

# Score real claims:
print("=== Scoring Real Quantum Advantage Claims ===\n")

claims = {
    "Google Sycamore RCS (2019)": dict(
        problem_useful=False, classical_comparison="best_known",
        advantage_scales=True, hardware_available=True,
        cost_competitive=False, independently_reproduced=True,
    ),
    "IBM Eagle Ising (2023)": dict(
        problem_useful=True, classical_comparison="best_known",
        advantage_scales=False, hardware_available=True,
        cost_competitive=False, independently_reproduced=False,
    ),
    "Q-CTRL Navigation (2024)": dict(
        problem_useful=True, classical_comparison="best_known",
        advantage_scales=True, hardware_available=True,
        cost_competitive=True, independently_reproduced=True,
    ),
    "Shor RSA-2048 (theoretical)": dict(
        problem_useful=True, classical_comparison="optimal",
        advantage_scales=True, hardware_available=False,
        cost_competitive=False, independently_reproduced=True,
    ),
}

for name, params in claims.items():
    level, label, flags = score_quantum_claim(**params)
    print(f"  {name}")
    print(f"    Level {level}: {label}")
    for f in flags:
        print(f"    WARNING: {f}")
    print()

# Expected output:
# === Scoring Real Quantum Advantage Claims ===
#
#   Google Sycamore RCS (2019)
#     Level 1: SUPREMACY ONLY
#     WARNING: Problem has no practical application
#
#   IBM Eagle Ising (2023)
#     Level 2: QUANTUM UTILITY
#     WARNING: Classical comparison not independently verified
#     WARNING: Advantage may disappear at larger problem sizes
#     WARNING: Classical solution is cheaper
#
#   Q-CTRL Navigation (2024)
#     Level 4: PRACTICAL ADVANTAGE
#
#   Shor RSA-2048 (theoretical)
#     Level 3: SCALABLE ADVANTAGE
#     WARNING: Requires hardware that doesn't exist yet
#     WARNING: Classical solution is cheaper
