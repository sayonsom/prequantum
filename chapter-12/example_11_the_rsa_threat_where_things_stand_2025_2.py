"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 3: The Concept Build > 3.8 The RSA Threat: Where Things Stand (2025-26)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_11_the_rsa_threat_where_things_stand_2025_2.py
"""

import numpy as np

# RSA key sizes and Shor's requirements -- UPDATED 2025-26
print("RSA key sizes vs. Shor's algorithm requirements (2025 estimates):\n")
print(f"{'Key bits':>10s} {'Classical (GNFS)':>18s} {'Logical qubits':>16s} {'Physical qubits':>18s} {'Runtime':>10s}")
print("-" * 78)

for bits in [512, 1024, 2048, 4096]:
    # Classical: General Number Field Sieve
    n = bits
    c = 1.9
    classical_ops = np.exp(c * (n * np.log(2))**(1/3) * (np.log(n * np.log(2)))**(2/3))

    # Shor's logical qubits (Beauregard: 2n+3)
    shor_logical = 2 * bits + 3

    # Physical qubits (2025 Gidney estimate scales roughly linearly)
    # RSA-2048 → <1M, so roughly 500 per bit
    shor_physical = int(bits * 488)  # ~1M for 2048

    # Runtime scales as n³ for the quantum part
    runtime_hours = (bits / 2048)**3 * 120  # ~5 days for RSA-2048

    if classical_ops > 1e100:
        classical_str = f">10^{int(np.log10(classical_ops))}"
    else:
        classical_str = f"~10^{int(np.log10(classical_ops))}"

    if runtime_hours < 1:
        runtime_str = f"{runtime_hours*60:.0f} min"
    elif runtime_hours < 24:
        runtime_str = f"{runtime_hours:.0f} hrs"
    else:
        runtime_str = f"{runtime_hours/24:.0f} days"

    print(f"{bits:10d} {classical_str:>18s} {shor_logical:>16,d} {shor_physical:>18,d} {runtime_str:>10s}")

# Current hardware state
print(f"\n{'=' * 78}")
print(f"QUANTUM HARDWARE STATUS (2025-26)")
print(f"{'=' * 78}")

hardware = [
    ("Google Willow", 2024, 105, "Superconducting", "Below-threshold QEC demonstrated"),
    ("IBM Nighthawk", 2025, 120, "Superconducting", "5,000 two-qubit gate circuits"),
    ("IBM Kookaburra", 2026, 4158, "Superconducting", "Multi-chip, 3×1,386 qubits"),
    ("IBM Starling", 2029, 10000, "Superconducting", "~200 logical qubits target"),
    ("IBM Blue Jay", 2033, 100000, "Superconducting", "~2,000 logical qubits target"),
]

print(f"\n{'System':<18s} {'Year':>6s} {'Physical qubits':>17s} {'Platform':<18s} {'Notes'}")
print("-" * 85)
for name, year, qubits, platform, notes in hardware:
    symbol = "  " if year <= 2025 else "→ "
    print(f"{symbol}{name:<16s} {year:6d} {qubits:17,d} {platform:<18s} {notes}")

print(f"\nGap: need ~1M physical qubits for RSA-2048. Best available: ~4,158 (Kookaburra, 2026)")
print(f"That's ~240× shortfall -- but several roadmaps target 1M+ by 2030-2033")
