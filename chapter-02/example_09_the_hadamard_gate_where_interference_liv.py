"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.3 The Hadamard Gate: Where Interference Lives
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_09_the_hadamard_gate_where_interference_liv.py
"""

class Qubit:
    """Full qubit with measurement and gates."""

    def __init__(self, state=None):
        if state is None:
            state = np.array([1, 0], dtype=complex)
        self.state = np.array(state, dtype=complex)
        self._normalize()

    def _normalize(self):
        norm = np.sqrt(np.sum(np.abs(self.state)**2))
        self.state = self.state / norm

    def measure(self, rng=None):
        if rng is None:
            rng = np.random.default_rng()
        prob_0 = abs(self.state[0])**2
        result = rng.choice([0, 1], p=[prob_0, 1 - prob_0])
        if result == 0:
            self.state = np.array([1, 0], dtype=complex)
        else:
            self.state = np.array([0, 1], dtype=complex)
        return result

    def hadamard(self):
        """Apply the Hadamard gate: matrix multiplication."""
        H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        self.state = H @ self.state  # Gate = matrix multiply
        return self

    def __repr__(self):
        return f"Qubit(state={np.round(self.state, 4)})"

# Start in "definitely 0", apply Hadamard
q = Qubit()
print(f"Before H: {q}")   # Qubit(state=[1.+0.j, 0.+0.j])

q.hadamard()
print(f"After H:  {q}")   # Qubit(state=[0.7071+0.j, 0.7071+0.j])
