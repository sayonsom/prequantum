"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 4: The AI Lab > Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_14_break_this.py
"""

import numpy as np

def broken_amplitude_encode(x):
    """Encode data as quantum amplitudes."""
    n = len(x)
    n_padded = 2**int(np.ceil(np.log2(max(n, 2))))
    state = np.zeros(n_padded, dtype=complex)
    state[:n] = x
    # "Normalize" by dividing by length
    state = state / len(state)
    return state

x = np.array([3.0, 4.0])
phi = broken_amplitude_encode(x)
print(f"State: {phi}")
print(f"Prob sum: {np.sum(np.abs(phi)**2):.4f}")  # Should be 1.0!
