"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.5 Beyond H₂: What Quantum Chemistry Looks Like at Scale
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_06_beyond_h₂_what_quantum_chemistry_looks_l.py
"""

import numpy as np

# Resource estimates for quantum chemistry simulation
# (Approximate values from literature -- actual numbers depend on
# basis set, active space, and algorithm choice)
molecules = [
    ("H₂ (STO-3G)",      2,    4,       20,       "Textbook demo"),
    ("LiH (STO-3G)",      4,   12,      200,       "Small benchmark"),
    ("H₂O (6-31G)",       8,   40,    3_000,       "IBM demo (2024)"),
    ("N₂ (cc-pVDZ)",     14,  100,   50_000,       "Nitrogen fixation"),
    ("Fe₂S₂ cluster",    40,  500, 5_000_000,       "Iron-sulfur biology"),
    ("FeMoco (active)",  ~54, ~200, "~10^9",        "Nitrogenase catalyst"),
]

print(f"{'Molecule':<22} {'Qubits':>7} {'Parameters':>11} {'CNOT gates':>12}  Application")
print("-" * 80)
for name, q, p, g, app in molecules:
    g_str = f"{g:>12,}" if isinstance(g, int) else f"{g:>12}"
    print(f"{name:<22} {q:>7} {p:>11,} {g_str}  {app}")

print("\n--- Key takeaway ---")
print("FeMoco (the active site of nitrogenase, the enzyme that fixes nitrogen)")
print("requires ~200 perfectly-operating logical qubits and billions of gates.")
print("Current hardware: 50-150 noisy physical qubits. The gap is real but shrinking.")
