"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.9 The Road Ahead: NISQ to Fault Tolerance
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_10_the_road_ahead_nisq_to_fault_tolerance.py
"""

# Timeline reality check: what can we do at each scale?
milestones = [
    {"year": 2024, "logical": 1,    "capability": "Error-corrected memory (Willow)",
     "useful_for": "Proof of concept"},
    {"year": 2025, "logical": 2,    "capability": "Fault-tolerant 2-qubit gates (Quantinuum)",
     "useful_for": "Proof of concept"},
    {"year": 2026, "logical": 10,   "capability": "Small fault-tolerant circuits",
     "useful_for": "Benchmarking, academic research"},
    {"year": 2029, "logical": 200,  "capability": "Medium-scale FT computation",
     "useful_for": "Quantum chemistry, small optimization"},
    {"year": 2033, "logical": 2000, "capability": "Large-scale FT computation",
     "useful_for": "Drug discovery, materials science"},
    {"year": "2035+","logical": "20000+", "capability": "Cryptographically relevant",
     "useful_for": "Shor's algorithm on RSA-2048"},
]

print("Fault-Tolerant Quantum Computing Roadmap")
print("=" * 75)
for m in milestones:
    print(f"\n  {m['year']}  |  ~{m['logical']} logical qubits")
    print(f"         |  {m['capability']}")
    print(f"         |  Useful for: {m['useful_for']}")
