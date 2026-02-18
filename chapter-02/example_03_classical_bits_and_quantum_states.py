"""
Pre Quantum - Chapter 02: Classical Bits to Qubits
Code Example: Beat 3: The Concept Build > 3.1 Classical Bits and Quantum States
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-02/example_03_classical_bits_and_quantum_states.py
"""

class Bit:
    """A classical bit. Nothing quantum here."""

    def __init__(self, value=0):
        assert value in (0, 1), "A bit must be 0 or 1"
        self.value = value

    def measure(self):
        """Read the bit. Always returns the same value."""
        return self.value

    def flip(self):
        """NOT gate: 0 becomes 1, 1 becomes 0."""
        self.value = 1 - self.value
        return self  # enables chaining: Bit(0).flip().measure()

    def __repr__(self):
        return f"Bit({self.value})"

# Classical bit in action
b = Bit(0)
print(b.measure())        # 0
print(b.measure())        # 0 -- same answer every time
print(b.flip().measure())  # 1
