"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.7 Error Mitigation: From Noisy to Useful
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_11_error_mitigation_from_noisy_to_useful.py
"""

import numpy as np

# Calibration data: prepare each basis state, measure many times
# This builds the confusion matrix M[i][j] = P(measure i | prepared j)
M = np.array([
    # Prepared: |00>  |01>  |10>  |11>
    [0.96, 0.02, 0.03, 0.01],  # Measured |00>
    [0.01, 0.94, 0.01, 0.03],  # Measured |01>
    [0.02, 0.01, 0.93, 0.02],  # Measured |10>
    [0.01, 0.03, 0.03, 0.94],  # Measured |11>
])

# Our noisy Bell state results (from hardware or our simulation above)
counts_noisy = {'00': 4770, '01': 247, '10': 286, '11': 4486}
total = sum(counts_noisy.values())
labels = ['00', '01', '10', '11']
measured_probs = np.array([counts_noisy[l] / total for l in labels])

print(f"Measured (noisy):  {measured_probs.round(4)}")

# Mitigate: solve M @ true_probs = measured_probs
M_inv = np.linalg.inv(M)
mitigated_probs = M_inv @ measured_probs

# Clip negative probabilities and renormalize
mitigated_probs = np.clip(mitigated_probs, 0, None)
mitigated_probs /= mitigated_probs.sum()

print(f"Mitigated:         {mitigated_probs.round(4)}")
print(f"Ideal:             [0.5000, 0.0000, 0.0000, 0.5000]")
# Output:
# Measured (noisy):  [0.4770 0.0247 0.0286 0.4486]
# Mitigated:         [0.4945 0.0065 0.0089 0.4901]
# Ideal:             [0.5000, 0.0000, 0.0000, 0.5000]
