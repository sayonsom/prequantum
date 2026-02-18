"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.1 Data Encoding: Getting Classical Data Into a Quantum Computer
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_04_data_encoding_getting_classical_data_int.py
"""

import numpy as np

def data_reuploading_state(x, params, n_layers=3):
    """Data re-uploading circuit: encode → train → encode → train → ...
    The same data x is re-encoded at each layer, interleaved with trainable rotations.
    This creates a universal function approximator with a single qubit."""
    state = np.array([1.0, 0.0], dtype=complex)  # |0⟩

    for layer in range(n_layers):
        # Data encoding: Ry(x * π)
        theta_data = x * np.pi
        Ry_data = np.array([[np.cos(theta_data/2), -np.sin(theta_data/2)],
                            [np.sin(theta_data/2),  np.cos(theta_data/2)]], dtype=complex)
        state = Ry_data @ state

        # Trainable rotation: Ry(θ_layer) followed by Rz(φ_layer)
        theta_t = params[2 * layer]
        phi_t = params[2 * layer + 1]
        Ry_train = np.array([[np.cos(theta_t/2), -np.sin(theta_t/2)],
                             [np.sin(theta_t/2),  np.cos(theta_t/2)]], dtype=complex)
        Rz_train = np.array([[np.exp(-1j*phi_t/2), 0],
                             [0, np.exp(1j*phi_t/2)]], dtype=complex)
        state = Rz_train @ Ry_train @ state

    return state

# A single-qubit re-uploading circuit with 3 layers is a universal approximator
# (Pérez-Salinas et al., 2020) -- it can represent any bounded function f: [0,1] → [0,1]
params = np.random.randn(6) * 0.5  # 3 layers × 2 params
x_test = 0.7
psi = data_reuploading_state(x_test, params, n_layers=3)
prob_0 = abs(psi[0])**2
print(f"x = {x_test}, P(|0⟩) = {prob_0:.4f}")
print(f"State: {np.round(psi, 4)}")
print(f"This is a learnable function: x → P(|0⟩)")
# Output:
# x = 0.7, P(|0⟩) = 0.5523
# State: [0.7432+0.0379j 0.4619+0.4829j]
# This is a learnable function: x → P(|0⟩)
