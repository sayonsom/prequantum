"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 3: The Concept Build > 3.5 The Investment Landscape: Bubbles and Breakthroughs
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_06_the_investment_landscape_bubbles_and_bre.py
"""

# Quantum computing investment data (2020-2025)
investment_data = {
    "VC Funding ($B)":        [0.8, 1.4, 1.2, 1.6, 2.6, 3.8],  # 2020-2025
    "Years":                  [2020, 2021, 2022, 2023, 2024, 2025],
    "Government ($B est.)":   [0.3, 0.4, 0.5, 0.5, 0.7, 1.2],
}

# Company valuations vs revenue
valuations = {
    "IonQ":        {"market_cap_B": 24.5, "revenue_M": 53, "ps_ratio": 462},
    "Rigetti":     {"market_cap_B": 13.0, "revenue_M": 15, "ps_ratio": 867},
    "D-Wave":      {"market_cap_B": 3.5,  "revenue_M": 12, "ps_ratio": 292},
}

print("Quantum Company Valuations vs Revenue (Late 2025)")
print(f"{'Company':<12} {'Market Cap':>12} {'Revenue':>12} {'P/S Ratio':>12}")
print("-" * 50)
for company, data in valuations.items():
    print(f"{company:<12} ${data['market_cap_B']:>9.1f}B "
          f"${data['revenue_M']:>9.0f}M {data['ps_ratio']:>11}x")

# For context
print(f"\nFor context: typical software company P/S ratio = 5-15x")
print(f"High-growth SaaS at peak hype = 30-50x")
print(f"Quantum pure-plays = 300-900x")

# Total industry revenue
print(f"\nQuantum industry total revenue (2024): ~$700M")
print(f"Quantum industry total revenue (2025, projected): ~$1B")
print(f"Total VC invested (2020-2025): ~$11.4B")
print(f"ROI so far: significantly negative")

# The honest question
print("\n--- The Bubble Question ---")
print("IonQ stock: +712% in one year (Jan 2025-Jan 2026)")
print("Revenue growth: ~40% YoY")
print("Gap between narrative and fundamentals: widening")
print("Verdict: price-to-sales ratios imply belief in")
print("  transformative quantum advantage within 5-10 years.")
print("  If that timeline slips, valuations will correct.")
