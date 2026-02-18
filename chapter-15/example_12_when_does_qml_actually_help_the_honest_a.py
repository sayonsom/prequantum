"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.6 When Does QML Actually Help? The Honest Assessment (2025-26 Edition)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_12_when_does_qml_actually_help_the_honest_a.py
"""

import numpy as np

# Demonstration: when quantum and classical kernels disagree
def rbf_kernel(x1, x2, gamma=1.0):
    """Classical RBF (Gaussian) kernel."""
    return np.exp(-gamma * np.linalg.norm(x1 - x2)**2)

def simple_quantum_kernel(x1, x2):
    """Angle-encoding quantum kernel on 2 qubits."""
    def encode(x):
        q1 = np.array([np.cos(x[0]*np.pi/2), np.sin(x[0]*np.pi/2)])
        q2 = np.array([np.cos(x[1]*np.pi/2), np.sin(x[1]*np.pi/2)])
        return np.kron(q1, q2)
    return np.abs(np.dot(encode(x1).conj(), encode(x2)))**2

# Compare on three pairs of points
pairs = [
    ("Close points", [0.1, 0.2], [0.15, 0.25]),
    ("Far points", [0.1, 0.1], [0.9, 0.9]),
    ("Diagonal flip", [0.1, 0.9], [0.9, 0.1]),
]

print(f"{'Pair':<20} {'RBF':>8} {'Quantum':>8} {'Agree?':>8}")
print("-" * 48)
for name, x1, x2 in pairs:
    k_rbf = rbf_kernel(np.array(x1), np.array(x2))
    k_qml = simple_quantum_kernel(np.array(x1), np.array(x2))
    agree = "Yes" if (k_rbf > 0.5) == (k_qml > 0.5) else "No"
    print(f"{name:<20} {k_rbf:8.4f} {k_qml:8.4f} {agree:>8}")
# Output:
# Pair                      RBF  Quantum   Agree?
# ------------------------------------------------
# Close points           0.9950   0.9877      Yes
# Far points             0.2780   0.0091      Yes
# Diagonal flip          0.2780   0.0091      Yes
