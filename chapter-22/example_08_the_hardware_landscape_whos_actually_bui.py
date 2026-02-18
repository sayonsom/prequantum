"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.7 The Hardware Landscape: Who's Actually Building This?
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_08_the_hardware_landscape_whos_actually_bui.py
"""

# Current state of play: physical qubit counts vs. logical qubit targets
import numpy as np

roadmap = {
    "Google Willow (2024)":      {"physical": 105,   "logical_demo": 1,    "code": "Surface d=7"},
    "IBM Heron r3 (2024)":       {"physical": 156,   "logical_demo": 0,    "code": "N/A (NISQ)"},
    "Quantinuum Helios (2025)":  {"physical": 56,    "logical_demo": 2,    "code": "Color code"},
    "IBM Kookaburra (2026)":     {"physical": 1386,  "logical_demo": "~10","code": "qLDPC"},
    "IBM Starling (2029)":       {"physical": "~100k","logical_demo": 200,  "code": "qLDPC"},
    "IBM Blue Jay (2033)":       {"physical": "~1M", "logical_demo": 2000, "code": "qLDPC"},
}

print(f"{'System':<30} {'Physical':>10} {'Logical':>10} {'Code Type':<15}")
print("-" * 70)
for name, spec in roadmap.items():
    print(f"{name:<30} {str(spec['physical']):>10} "
          f"{str(spec['logical_demo']):>10} {spec['code']:<15}")

# What do useful algorithms need?
print("\n--- What algorithms actually require ---")
algorithms = {
    "Shor's (RSA-2048)":     {"logical": "4,000-20,000", "physical_est": "~4-20M"},
    "Grover's (useful)":     {"logical": "~1,000",       "physical_est": "~1-2M"},
    "VQE (large molecule)":  {"logical": "~200-500",     "physical_est": "~200k-1M"},
    "QAOA (advantage)":      {"logical": "~100-500",     "physical_est": "~100k-500k"},
}
print(f"{'Algorithm':<25} {'Logical Qubits':>15} {'Physical Est.':>15}")
print("-" * 58)
for algo, req in algorithms.items():
    print(f"{algo:<25} {req['logical']:>15} {req['physical_est']:>15}")

# Output:
# System                         Physical    Logical Code Type
# ----------------------------------------------------------------------
# Google Willow (2024)                105          1 Surface d=7
# IBM Heron r3 (2024)                 156          0 N/A (NISQ)
# Quantinuum Helios (2025)             56          2 Color code
# IBM Kookaburra (2026)              1386        ~10 qLDPC
# IBM Starling (2029)              ~100k        200 qLDPC
# IBM Blue Jay (2033)                ~1M       2000 qLDPC
#
# --- What algorithms actually require ---
# Algorithm                 Logical Qubits  Physical Est.
# ----------------------------------------------------------
# Shor's (RSA-2048)          4,000-20,000       ~4-20M
# Grover's (useful)               ~1,000         ~1-2M
# VQE (large molecule)          ~200-500     ~200k-1M
# QAOA (advantage)              ~100-500    ~100k-500k
