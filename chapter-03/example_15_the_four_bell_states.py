"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.6 The Four Bell States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_15_the_four_bell_states.py
"""

import numpy as np
from collections import Counter

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
I = np.eye(2, dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
H_on_q0 = np.kron(H, I)

def make_bell_state(q0_state, q1_state):
    """H on qubit 0, then CNOT."""
    state = np.kron(np.array(q0_state, dtype=complex),
                    np.array(q1_state, dtype=complex))
    return CNOT @ (H_on_q0 @ state)

def measure_system(state, n_shots=10000, seed=42):
    rng = np.random.default_rng(seed)
    probs = np.abs(state)**2
    outcomes = rng.choice(4, size=n_shots, p=probs)
    labels = {0: "00", 1: "01", 2: "10", 3: "11"}
    return Counter(labels[o] for o in outcomes)

bell_states = {
    "Phi+": make_bell_state([1, 0], [1, 0]),  # start |00>
    "Phi-": make_bell_state([0, 1], [1, 0]),  # start |10>
    "Psi+": make_bell_state([1, 0], [0, 1]),  # start |01>
    "Psi-": make_bell_state([0, 1], [0, 1]),  # start |11>
}

for name, state in bell_states.items():
    counts = measure_system(state)
    outcomes_seen = sorted(k for k, v in counts.items() if v > 0)
    print(f"{name}: {np.round(state, 4)}  ->  outcomes: {outcomes_seen}")
