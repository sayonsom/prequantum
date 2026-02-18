"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.2 Measurement: Random, Irreversible, and Strange
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_06_measurement_random_irreversible_and_stra.py
"""

class Qubit:
    """A quantum bit with measurement."""

    def __init__(self, state=None):
        if state is None:
            state = np.array([1, 0], dtype=complex)
        self.state = np.array(state, dtype=complex)
        self._normalize()

    def _normalize(self):
        norm = np.sqrt(np.sum(np.abs(self.state)**2))
        self.state = self.state / norm

    def measure(self, rng=None):
        """Measure the qubit. Returns 0 or 1. Collapses the state."""
        if rng is None:
            rng = np.random.default_rng()

        prob_0 = abs(self.state[0])**2
        result = rng.choice([0, 1], p=[prob_0, 1 - prob_0])

        # Collapse: state becomes definite
        if result == 0:
            self.state = np.array([1, 0], dtype=complex)
        else:
            self.state = np.array([0, 1], dtype=complex)

        return result

    def __repr__(self):
        return f"Qubit(state={self.state})"
