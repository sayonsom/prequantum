"""
Pre Quantum - Chapter 03: Entanglement and Quantum States
Code Example: Beat 3: The Concept Build > 3.3 The CNOT Gate: Conditional Logic for Qubits
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-03/example_08_the_cnot_gate_conditional_logic_for_qubi.py
"""

import numpy as np

# CNOT gate matrix (control = qubit 0, target = qubit 1)
CNOT = np.array([
    [1, 0, 0, 0],  # |00> -> |00>  (control=0, do nothing)
    [0, 1, 0, 0],  # |01> -> |01>  (control=0, do nothing)
    [0, 0, 0, 1],  # |10> -> |11>  (control=1, flip target!)
    [0, 0, 1, 0],  # |11> -> |10>  (control=1, flip target!)
], dtype=complex)

# Test each input
inputs = {
    "00": np.array([1, 0, 0, 0], dtype=complex),
    "01": np.array([0, 1, 0, 0], dtype=complex),
    "10": np.array([0, 0, 1, 0], dtype=complex),
    "11": np.array([0, 0, 0, 1], dtype=complex),
}

for label, state in inputs.items():
    result = CNOT @ state
    out_idx = np.argmax(np.abs(result))
    out_label = ["00", "01", "10", "11"][out_idx]
    print(f"  CNOT |{label}> -> |{out_label}>")
# CNOT |00> -> |00>
# CNOT |01> -> |01>
# CNOT |10> -> |11>  <- target flipped!
# CNOT |11> -> |10>  <- target flipped!
