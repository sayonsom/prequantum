"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 3: The Concept Build > 3.6 The Decision Framework: Should Your Company Invest?
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_07_the_decision_framework_should_your_compa.py
"""

def should_invest_in_quantum(
    problem_type: str,
    problem_size: str,
    time_horizon: str,
    budget: str,
    classical_satisfactory: bool,
):
    """
    Decision framework for quantum computing investment.
    Returns recommendation and reasoning.
    """
    recommendations = []

    # Filter 1: Problem type
    quantum_fit = {
        "optimization": "possible",        # QAOA, but classical often wins
        "chemistry_simulation": "strong",   # VQE, strong theoretical advantage
        "machine_learning": "weak",         # dequantization, limited evidence
        "cryptography": "strong",           # Shor's, QKD (but PQC exists)
        "sensing": "proven",               # demonstrable today
        "financial_modeling": "weak",       # hype exceeds evidence
        "grid_optimization": "possible",   # structured QUBO, needs scale
    }
    fit = quantum_fit.get(problem_type, "unknown")

    if fit == "weak" or fit == "unknown":
        recommendations.append(
            f"WAIT: Quantum advantage for {problem_type} is unproven. "
            f"Invest in classical ML/optimization instead."
        )
        return "DO NOT INVEST YET", recommendations

    if classical_satisfactory:
        recommendations.append(
            "CAUTION: If classical solutions work, quantum is a risk, not a fix."
        )

    # Filter 2: Time horizon
    if time_horizon == "now":
        if fit != "proven":
            recommendations.append(
                "WAIT: No practical quantum advantage available today "
                "except in quantum sensing."
            )
            return "DO NOT INVEST YET", recommendations
    elif time_horizon == "3-5 years":
        if fit in ("strong", "proven"):
            recommendations.append(
                "EXPLORE: Build internal expertise. Run proof-of-concepts. "
                "Don't bet production workloads on quantum."
            )
            return "EXPLORE (small budget)", recommendations
    elif time_horizon == "5-10 years":
        if fit in ("strong", "possible", "proven"):
            recommendations.append(
                "INVEST: Build team, establish partnerships with hardware vendors, "
                "identify 2-3 pilot problems."
            )
            return "INVEST (moderate budget)", recommendations

    # Filter 3: Budget reality check
    if budget == "small":
        recommendations.append(
            "START LEARNING: Use free cloud access (IBM Quantum, Amazon Braket free tier). "
            "Train 1-2 developers. Cost: near zero."
        )
    elif budget == "medium":
        recommendations.append(
            "BUILD CAPABILITY: Dedicated quantum team (2-3 people), "
            "cloud access to real hardware, proof-of-concept projects."
        )
    elif budget == "large":
        recommendations.append(
            "STRATEGIC INVESTMENT: On-premise access, hardware partnerships, "
            "dedicated research program. But track ROI honestly."
        )

    return "CONDITIONAL INVEST", recommendations

# Example: utility company considering quantum for grid optimization
print("=== Decision: Utility Company + Grid Optimization ===\n")
decision, reasons = should_invest_in_quantum(
    problem_type="grid_optimization",
    problem_size="large",
    time_horizon="5-10 years",
    budget="medium",
    classical_satisfactory=True,
)
print(f"Recommendation: {decision}")
for r in reasons:
    print(f"  - {r}")

print("\n=== Decision: Pharma Company + Drug Discovery ===\n")
decision, reasons = should_invest_in_quantum(
    problem_type="chemistry_simulation",
    problem_size="large",
    time_horizon="3-5 years",
    budget="large",
    classical_satisfactory=False,
)
print(f"Recommendation: {decision}")
for r in reasons:
    print(f"  - {r}")

# Expected output:
# === Decision: Utility Company + Grid Optimization ===
#
# Recommendation: CONDITIONAL INVEST
#   - CAUTION: If classical solutions work, quantum is a risk, not a fix.
#   - BUILD CAPABILITY: Dedicated quantum team (2-3 people), cloud access
#     to real hardware, proof-of-concept projects.
#
# === Decision: Pharma Company + Drug Discovery ===
#
# Recommendation: EXPLORE (small budget)
#   - EXPLORE: Build internal expertise. Run proof-of-concepts.
#     Don't bet production workloads on quantum.
