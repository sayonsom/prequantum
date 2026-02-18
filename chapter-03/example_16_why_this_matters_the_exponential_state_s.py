"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.7 Why This Matters: The Exponential State Space
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_16_why_this_matters_the_exponential_state_s.py
"""

import numpy as np

for n in [1, 2, 5, 10, 20, 30, 40, 50]:
    amps = 2**n
    mem_gb = amps * 16 / 1e9  # 16 bytes per complex128
    print(f"  {n:2d} qubits -> {amps:>16,} amplitudes  ({mem_gb:>10.1f} GB)")
