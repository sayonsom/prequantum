"""
Pre Quantum - Chapter 07: Noise Errors and Why Quantum is Hard
Code Example: Beat 3: The Concept Build > 3.4 The Error Budget: How Deep Can Your Circuits Go?
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-07/example_07_the_error_budget_how_deep_can_your_circu.py
"""

import numpy as np

# Hardware parameters circa 2025-2026
params = {
    "IBM Heron r3 (156q)": {
        "1q_error": 0.0003,   # 0.03%
        "2q_error": 0.002,    # 0.2% (best pairs below 0.1%)
        "t1_us": 250,
        "t2_us": 150,
        "gate_time_1q_ns": 36,
        "gate_time_2q_ns": 68,   # CZ native gate
        "native_2q": "CZ",
    },
    "IBM Nighthawk (120q)": {
        "1q_error": 0.0002,
        "2q_error": 0.0015,
        "t1_us": 350,
        "t2_us": 200,
        "gate_time_1q_ns": 36,
        "gate_time_2q_ns": 68,
        "native_2q": "CZ",
    },
    "Google Willow (105q)": {
        "1q_error": 0.001,    # 0.1%
        "2q_error": 0.003,    # 0.3%
        "t1_us": 68,
        "t2_us": 40,
        "gate_time_1q_ns": 25,
        "gate_time_2q_ns": 32,    # iSWAP-like
        "native_2q": "iSWAP",
    },
    "Quantinuum Helios (98q ions)": {
        "1q_error": 0.00003,  # 0.003%
        "2q_error": 0.0005,   # 0.05%
        "t1_us": 10_000_000,  # ~10 seconds
        "t2_us": 1_000_000,   # ~1 second
        "gate_time_1q_ns": 10_000,  # ~10 μs
        "gate_time_2q_ns": 200_000, # ~200 μs
        "native_2q": "ZZMax",
    },
}

print("=== Error Budgets (2025-2026 Hardware) ===\n")

for name, p in params.items():
    # How many 2-qubit gates before fidelity drops below 50%?
    max_2q_gates = np.log(0.5) / np.log(1 - p["2q_error"])

    # How many 2q gates fit within T2?
    max_2q_in_t2 = (p["t2_us"] * 1000) / p["gate_time_2q_ns"]

    # Operations per coherence time (figure of merit)
    ops_per_t2 = max_2q_in_t2

    print(f"{name}:")
    print(f"  1q gate error:    {p['1q_error']*100:.3f}%")
    print(f"  2q gate error:    {p['2q_error']*100:.2f}%  (native: {p['native_2q']})")
    print(f"  T1/T2:            {p['t1_us']:.0f} / {p['t2_us']:.0f} μs")
    print(f"  Max 2q gates (50% fidelity):  ~{max_2q_gates:.0f}")
    print(f"  Max 2q gates in T2 window:    ~{max_2q_in_t2:.0f}")
    print(f"  Bottleneck: {'gate errors' if max_2q_gates < max_2q_in_t2 else 'decoherence'}")
    print()
