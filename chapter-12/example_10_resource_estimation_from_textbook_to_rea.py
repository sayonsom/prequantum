"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.7 Resource Estimation: From Textbook to Real Hardware
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_10_resource_estimation_from_textbook_to_rea.py
"""

import numpy as np

# Resource estimation for factoring RSA-2048 with Shor's algorithm

print("=" * 80)
print("RESOURCE ESTIMATES FOR FACTORING RSA-2048")
print("=" * 80)

n = 2048  # RSA key size in bits

# Logical-level requirements
logical_qubits_beauregard = 2 * n + 3  # Beauregard 2003
logical_qubits_chevignard = int(0.85 * n)  # Chevignard et al. 2024
toffoli_gates = n**3  # order of magnitude
print(f"\nLogical-level requirements:")
print(f"  Beauregard (2003): {logical_qubits_beauregard:,} logical qubits")
print(f"  Chevignard et al. (2024): ~{logical_qubits_chevignard:,} logical qubits")
print(f"  Toffoli gates: ~n³ = ~{toffoli_gates:.2e}")

# Physical qubit overhead with surface codes
print(f"\nPhysical qubit estimates (surface code, various error rates):")
print(f"{'Physical error rate':>22s}  {'Code distance':>14s}  {'Phys/logical':>14s}  {'Total physical':>16s}")
print("-" * 72)

for p_phys in [1e-3, 5e-4, 1e-4]:
    # Surface code: logical error rate ≈ (p_phys / p_threshold)^(d/2)
    # where d is code distance, p_threshold ≈ 1%
    p_threshold = 0.01
    # Need logical error rate < 1/total_gates for algorithm success
    target_logical_error = 1 / toffoli_gates

    # Solve for d: (p_phys/p_threshold)^(d/2) < target
    ratio = p_phys / p_threshold
    d = int(2 * np.log(target_logical_error) / np.log(ratio)) + 1
    if d % 2 == 0:
        d += 1  # code distance must be odd

    phys_per_logical = 2 * d**2  # surface code: ~2d² physical qubits per logical
    total_phys = logical_qubits_beauregard * phys_per_logical

    print(f"{p_phys:22.1e}  {d:14d}  {phys_per_logical:14,d}  {total_phys:16,d}")

# Historical progression of resource estimates
print(f"\n{'=' * 80}")
print(f"HISTORICAL PROGRESSION OF RESOURCE ESTIMATES FOR RSA-2048")
print(f"{'=' * 80}")

estimates = [
    (2003, "Beauregard", "4,099 logical qubits", "~1 billion physical", "Sequential circuit"),
    (2012, "Jones et al.", "~4,000 logical", "~1 billion physical", "Surface code estimates"),
    (2019, "Gidney & Ekerå", "~3,000 logical", "20 million physical", "Windowed arithmetic + distillation"),
    (2024, "Chevignard et al.", "~1,730 logical", "—", "Approximate residue arithmetic"),
    (2025, "Gidney", "~3,000 logical", "<1 million physical", "Magic state cultivation + yoked codes"),
]

print(f"\n{'Year':>6s}  {'Authors':<20s}  {'Logical qubits':<22s}  {'Physical qubits':<22s}  {'Key innovation'}")
print("-" * 105)
for year, authors, logical, physical, innovation in estimates:
    print(f"{year:6d}  {authors:<20s}  {logical:<22s}  {physical:<22s}  {innovation}")

print(f"\nThe trajectory: ~1 billion physical qubits (2012) → <1 million (2025)")
print(f"A 1000× improvement in 13 years, driven by algorithmic + error correction advances")
