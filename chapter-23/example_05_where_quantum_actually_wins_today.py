"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 3: The Concept Build > 3.4 Where Quantum Actually Wins (Today)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_05_where_quantum_actually_wins_today.py
"""

# Where quantum wins: application maturity scorecard
applications = {
    "Random circuit sampling": {
        "advantage_level": 1, "maturity": "Demonstrated",
        "timeline": "Now", "practical_value": "None",
        "confidence": "High (but debated)",
    },
    "Quantum sensing / metrology": {
        "advantage_level": 4, "maturity": "Commercial",
        "timeline": "Now", "practical_value": "High (defense, navigation)",
        "confidence": "High",
    },
    "Quantum key distribution": {
        "advantage_level": 3, "maturity": "Deployed",
        "timeline": "Now", "practical_value": "Moderate (niche)",
        "confidence": "High (physics-based)",
    },
    "Quantum chemistry (small)": {
        "advantage_level": 2, "maturity": "Research",
        "timeline": "2027-2030", "practical_value": "High (pharma, materials)",
        "confidence": "Medium",
    },
    "Optimization (QAOA/VQE)": {
        "advantage_level": 1, "maturity": "Research",
        "timeline": "2030+", "practical_value": "High if achieved",
        "confidence": "Low (barren plateaus, classical competition)",
    },
    "Shor's factoring": {
        "advantage_level": 3, "maturity": "Theoretical",
        "timeline": "2035+", "practical_value": "High (security)",
        "confidence": "High (proven, needs hardware)",
    },
    "Machine learning (QML)": {
        "advantage_level": 1, "maturity": "Research",
        "timeline": "Unknown", "practical_value": "Unknown",
        "confidence": "Low (dequantization results)",
    },
    "Grid optimization (qgo)": {
        "advantage_level": 1, "maturity": "Research",
        "timeline": "2032+", "practical_value": "High if achieved",
        "confidence": "Low-Medium (structured QUBO, classical solvers strong)",
    },
}

print(f"{'Application':<32} {'Level':>5} {'Timeline':<12} {'Confidence':<10}")
print("-" * 65)
for app, data in applications.items():
    print(f"{app:<32} {data['advantage_level']:>5} "
          f"{data['timeline']:<12} {data['confidence']:<10}")

# Expected output:
# Application                      Level Timeline     Confidence
# -----------------------------------------------------------------
# Random circuit sampling               1 Now          High (...)
# Quantum sensing / metrology           4 Now          High
# Quantum key distribution              3 Now          High (...)
# Quantum chemistry (small)             2 2027-2030    Medium
# Optimization (QAOA/VQE)               1 2030+        Low (...)
# Shor's factoring                      3 2035+        High (...)
# Machine learning (QML)                1 Unknown      Low (...)
# Grid optimization (qgo)               1 2032+        Low-Medium
