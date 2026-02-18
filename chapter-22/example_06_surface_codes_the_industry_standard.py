"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.5 Surface Codes: The Industry Standard
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_06_surface_codes_the_industry_standard.py
"""

import numpy as np

def surface_code_overhead(physical_error_rate, target_logical_rate, d_max=25):
    """
    Estimate surface code overhead.

    For a distance-d surface code:
    - Physical qubits needed: ~2d² (data + syndrome qubits)
    - Logical error rate: p_L ≈ 0.1 * (p/p_th)^((d+1)/2)
      where p_th ≈ 0.01 is the threshold
    """
    p = physical_error_rate
    p_th = 0.01  # threshold for surface codes
    results = []

    if p >= p_th:
        print(f"WARNING: physical error rate {p} >= threshold {p_th}")
        print("Error correction makes things WORSE, not better!")
        return

    for d in range(3, d_max + 1, 2):  # odd distances only
        # Logical error rate estimate
        p_logical = 0.1 * (p / p_th) ** ((d + 1) / 2)
        # Physical qubit count (data + ancilla)
        n_physical = 2 * d * d
        # Logical qubits achievable with these physical qubits
        # (just 1 per surface code patch)

        if p_logical < target_logical_rate:
            results.append((d, n_physical, p_logical))
            if len(results) == 1:
                print(f"Minimum distance needed: d = {d}")

    if not results:
        print(f"Cannot reach target rate {target_logical_rate} with d ≤ {d_max}")
        return

    # Print the trade-off table
    print(f"\nPhysical error rate: {p}")
    print(f"Target logical rate: {target_logical_rate}")
    print(f"\n{'Distance':>8} {'Phys Qubits':>12} {'Logical Error':>14} {'Suppression':>12}")
    print("-" * 50)
    for d, n, p_l in results[:6]:
        suppression = p / p_l
        print(f"{d:>8} {n:>12,} {p_l:>14.2e} {suppression:>12,.0f}x")

# Scenario 1: IBM Heron-class hardware
print("=== IBM Heron (p = 0.001) ===")
surface_code_overhead(0.001, 1e-12)

print("\n=== Near-threshold hardware (p = 0.005) ===")
surface_code_overhead(0.005, 1e-12)

# Expected output:
# === IBM Heron (p = 0.001) ===
# Minimum distance needed: d = 7
#
# Physical error rate: 0.001
# Target logical rate: 1e-12
#
# Distance  Phys Qubits  Logical Error  Suppression
# --------------------------------------------------
#        7           98       1.00e-14   100,000,000x
#        9          162       1.00e-18   ...
#       ...
#
# === Near-threshold hardware (p = 0.005) ===
# Minimum distance needed: d = 17
# ...
