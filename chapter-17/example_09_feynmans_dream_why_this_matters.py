"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.8 Feynman's Dream: Why This Matters
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_09_feynmans_dream_why_this_matters.py
"""

import numpy as np

# Scaling comparison: classical memory vs quantum qubits
print(f"{'n particles':>12}  {'Classical entries':>18}  {'Qubits needed':>14}  {'RAM (16B/entry)':>20}")
print("-" * 68)
for n in [10, 20, 30, 40, 50, 65, 100, 300]:
    entries = 2**n
    ram_gb = entries * 16 / 1e9  # 16 bytes per complex128
    qubits = n
    if ram_gb < 0.001:
        ram_str = f"{ram_gb*1e6:.0f} KB"
    elif ram_gb < 1:
        ram_str = f"{ram_gb*1000:.1f} MB"
    elif ram_gb < 1e3:
        ram_str = f"{ram_gb:.1f} GB"
    elif ram_gb < 1e6:
        ram_str = f"{ram_gb/1e3:.1f} TB"
    elif ram_gb < 1e9:
        ram_str = f"{ram_gb/1e6:.1f} PB"
    else:
        ram_str = f"10^{np.log10(ram_gb):.0f} GB"
    label = ""
    if n == 40:
        label = "  ← supercomputer limit"
    elif n == 65:
        label = "  ← Google Quantum Echoes (2025)"
    elif n == 100:
        label = "  ← no classical computer ever"
    print(f"{n:>12}  {entries:>18,.0f}  {qubits:>14}{ram_str:>20}{label}")
# Output:
# n particles  Classical entries   Qubits needed  RAM (16B/entry)
# --------------------------------------------------------------------
#          10             1,024              10              16 KB
#          20         1,048,576              20            16.8 MB
#          30     1,073,741,824              30            17.2 GB
#          40 1,099,511,627,776              40            17.6 TB  ← supercomputer limit
#          50               ...              50            18.0 PB
#          65               ...              65  ← Google Quantum Echoes (2025)
#         100               ...             100          10^21 GB  ← no classical computer ever
#         300               ...             300          10^81 GB
