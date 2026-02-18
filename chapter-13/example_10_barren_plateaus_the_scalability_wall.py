"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.8 Barren Plateaus: The Scalability Wall
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_10_barren_plateaus_the_scalability_wall.py
"""

# Conceptual comparison of barren plateau mitigation strategies
# (Pseudocode -- illustrates the ideas, not production implementations)

strategies = {
    "Standard VQE": {
        "description": "Random init, fixed ansatz, global optimizer",
        "gradient_preservation": "None",
        "wall_clock": "Baseline",
    },
    "Layer-by-layer (Local-Global)": {
        "description": "Train one layer at a time, then fine-tune globally",
        "gradient_preservation": "High initially, decays with depth",
        "wall_clock": "~2x baseline",
    },
    "Adiabatic-inspired": {
        "description": "Start with easy Hamiltonian, slowly deform to target",
        "gradient_preservation": "Moderate -- smooth energy landscape",
        "wall_clock": "~3x baseline (many intermediate Hamiltonians)",
    },
    "State Efficient Ansatz (SEA)": {
        "description": "Ansatz preserves particle number / symmetries",
        "gradient_preservation": "High -- restricted search space",
        "wall_clock": "~1.5x baseline (fewer parameters to optimize)",
    },
    "Pretrained VQE": {
        "description": "Use ML to predict good initial parameters",
        "gradient_preservation": "Starts near solution → large gradients",
        "wall_clock": "Requires offline training, but fast at runtime",
    },
}

# Key finding from the 2025 benchmarking study (Arxiv 2512.11171):
# Performance is ITERATION-DEPENDENT.
# At 100 iterations: Pretrained VQE wins (good init matters most)
# At 1000 iterations: SEA wins (smaller search space → more efficient)
# Lesson: match strategy to your compute budget, not just gradient variance.

print(f"{'Strategy':<30s} {'Best at low budget':>20s} {'Best at high budget':>20s}")
print("-" * 72)
for name, info in strategies.items():
    low = "✓" if name == "Pretrained VQE" else ""
    high = "✓" if name == "State Efficient Ansatz (SEA)" else ""
    print(f"{name:<30s} {low:>20s} {high:>20s}")
