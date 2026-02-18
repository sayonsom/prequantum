"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 3: The Concept Build > 3.2 The Classical Algorithm Moving Target
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_03_the_classical_algorithm_moving_target.py
"""

# Timeline: classical algorithms closing the gap on quantum claims
timeline = [
    {"year": 2019, "event": "Google Sycamore: 200s quantum vs '10,000 years' classical",
     "classical_est": "10,000 years"},
    {"year": 2020, "event": "IBM: tensor network methods reduce estimate",
     "classical_est": "2.5 days"},
    {"year": 2021, "event": "Pan & Zhang: improved contraction ordering",
     "classical_est": "15 hours"},
    {"year": 2022, "event": "GPU-optimized tensor networks",
     "classical_est": "~1 hour"},
    {"year": 2024, "event": "1,432 GPUs on Frontier supercomputer",
     "classical_est": "86 seconds"},
]

print("Classical catch-up for Google Sycamore RCS task:")
print(f"{'Year':<6} {'Classical Estimate':<20} {'Speed vs Quantum':<20}")
print("-" * 48)
for entry in timeline:
    print(f"{entry['year']:<6} {entry['classical_est']:<20}")

print(f"\nReduction: 10,000 years → 86 seconds in 5 years")
print(f"Factor: ~3.7 billion x faster")
