"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.4 From Simulator to Silicon: Transpilation Deep Dive
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_08_from_simulator_to_silicon_transpilation.py
"""

import numpy as np

# Error accumulation from transpilation overhead
# IBM Heron r3 (July 2025): median 2Q error ~2.15e-3, best pairs <1e-3
cz_error_rate_median = 0.00215  # median across chip
cz_error_rate_best = 0.001     # best qubit pairs

print("Error accumulation (Heron r3 median vs. best pairs):")
for n_extra_czs in [0, 3, 6, 9, 12]:
    success_median = (1 - cz_error_rate_median) ** n_extra_czs
    success_best = (1 - cz_error_rate_best) ** n_extra_czs
    print(f"  +{n_extra_czs:>2} CZs (from {n_extra_czs//3} SWAPs): "
          f"median {1-success_median:.3%} error, "
          f"best {1-success_best:.3%} error")
# Output:
#   + 0 CZs (from 0 SWAPs): 0.000% error, 0.000% error
#   + 3 CZs (from 1 SWAPs): 0.643% error, 0.300% error
#   + 6 CZs (from 2 SWAPs): 1.282% error, 0.599% error
#   + 9 CZs (from 3 SWAPs): 1.917% error, 0.897% error
#   +12 CZs (from 4 SWAPs): 2.549% error, 1.194% error
