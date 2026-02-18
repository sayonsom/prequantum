"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 3: The Concept Build > 3.1 Why Quantum Error Correction is Hard
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_02_why_quantum_error_correction_is_hard.py
"""

import numpy as np

# Encoding: |ψ⟩ = α|0⟩ + β|1⟩ → α|000⟩ + β|111⟩
# This is NOT cloning. Watch:

alpha, beta = 1/np.sqrt(3), np.sqrt(2/3)  # arbitrary state

# Cloning would produce: (α|0⟩ + β|1⟩) ⊗ (α|0⟩ + β|1⟩) ⊗ (α|0⟩ + β|1⟩)
# = α³|000⟩ + α²β|001⟩ + α²β|010⟩ + ... (8 terms)
cloned = np.kron(np.kron([alpha, beta], [alpha, beta]), [alpha, beta])
print(f"Cloned state has {np.count_nonzero(np.abs(cloned) > 1e-10)} non-zero amplitudes")

# Encoding produces: α|000⟩ + β|111⟩  (only 2 terms!)
encoded = np.zeros(8)
encoded[0b000] = alpha  # |000⟩
encoded[0b111] = beta   # |111⟩
print(f"Encoded state has {np.count_nonzero(np.abs(encoded) > 1e-10)} non-zero amplitudes")
print(f"Are they the same? {np.allclose(cloned, encoded)}")

# Output:
# Cloned state has 8 non-zero amplitudes
# Encoded state has 2 non-zero amplitudes
# Are they the same? False
