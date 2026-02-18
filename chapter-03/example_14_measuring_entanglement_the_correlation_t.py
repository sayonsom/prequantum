"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.5 Measuring Entanglement: The Correlation Test
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_14_measuring_entanglement_the_correlation_t.py
"""

import numpy as np
from collections import Counter

def measure_system(state, n_shots=10000, seed=42):
    """Measure a 2-qubit system n_shots times."""
    rng = np.random.default_rng(seed)
    probs = np.abs(state)**2
    outcomes = rng.choice(4, size=n_shots, p=probs)
    labels = {0: "00", 1: "01", 2: "10", 3: "11"}
    return Counter(labels[o] for o in outcomes)

def correlation(results, n_shots):
    """
    +1 = always agree, -1 = always disagree, 0 = independent.
    """
    agree = results.get("00", 0) + results.get("11", 0)
    disagree = results.get("01", 0) + results.get("10", 0)
    return (agree - disagree) / n_shots

# ---- Entangled (Bell Phi+) ----
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

entangled = CNOT @ (np.kron(H, I) @ np.array([1,0,0,0], dtype=complex))
ent_results = measure_system(entangled)

print("Entangled (Bell Phi+):")
for label in ["00", "01", "10", "11"]:
    print(f"  {label}: {ent_results.get(label, 0)}")
print(f"  Correlation: {correlation(ent_results, 10000):.4f}")

# ---- Independent superpositions ----
independent = np.kron(
    np.array([1, 1], dtype=complex) / np.sqrt(2),
    np.array([1, 1], dtype=complex) / np.sqrt(2)
)
ind_results = measure_system(independent)

print("\nIndependent superpositions:")
for label in ["00", "01", "10", "11"]:
    print(f"  {label}: {ind_results.get(label, 0)}")
print(f"  Correlation: {correlation(ind_results, 10000):.4f}")
