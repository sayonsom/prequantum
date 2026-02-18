"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.1 Classical Bits and Quantum States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_04_classical_bits_and_quantum_states.py
"""

import numpy as np

class Qubit:
    """A quantum bit. State is a 2-element numpy array."""

    def __init__(self, state=None):
        if state is None:
            state = np.array([1, 0], dtype=complex)  # Default: "definitely 0"
        self.state = np.array(state, dtype=complex)
        self._normalize()

    def _normalize(self):
        """Ensure probabilities sum to 1."""
        norm = np.sqrt(np.sum(np.abs(self.state)**2))
        self.state = self.state / norm

    def __repr__(self):
        return f"Qubit(state={self.state})"

# A qubit that's definitely 0
q = Qubit()
print(q)  # Qubit(state=[1.+0.j, 0.+0.j])

# A qubit that's definitely 1
q1 = Qubit([0, 1])
print(q1)  # Qubit(state=[0.+0.j, 1.+0.j])

# A qubit in superposition -- equal chance of 0 or 1
q_super = Qubit([1, 1])
print(q_super)  # Qubit(state=[0.70710678+0.j, 0.70710678+0.j])
