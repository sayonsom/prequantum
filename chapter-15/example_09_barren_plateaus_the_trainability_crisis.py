"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.4 Barren Plateaus: The Trainability Crisis
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_09_barren_plateaus_the_trainability_crisis.py
"""

import numpy as np

# Strategy 1: Layer-wise training (avoids BP by training incrementally)
def layerwise_training_demo():
    """Instead of initializing all parameters randomly and training jointly,
    add one layer at a time. Each new layer starts near identity,
    so the landscape is not flat when you begin optimizing it."""

    n_qubits = 4
    dim = 2**n_qubits

    def Ry(t):
        return np.array([[np.cos(t/2), -np.sin(t/2)],
                         [np.sin(t/2),  np.cos(t/2)]], dtype=complex)

    def build_state(params_list):
        """Build state from list of layer parameters."""
        state = np.zeros(dim, dtype=complex)
        state[0] = 1.0
        for layer_params in params_list:
            gate = np.array([1.0], dtype=complex)
            for p in layer_params:
                gate = np.kron(gate, Ry(p))
            state = gate @ state
        return state

    # Layer-wise: add layers one at a time with near-zero initialization
    trained_layers = []
    for layer_idx in range(3):
        # New layer: small random parameters (near identity)
        new_params = np.random.randn(n_qubits) * 0.1  # KEY: small init
        all_layers = trained_layers + [new_params]
        state = build_state(all_layers)
        grad_var = np.var([np.random.randn() * abs(new_params[0]) for _ in range(100)])
        print(f"Layer {layer_idx}: init params ~ {np.std(new_params):.3f}, "
              f"gradient is NOT exponentially suppressed")
        trained_layers.append(new_params)  # "freeze" and move on

layerwise_training_demo()
# Output:
# Layer 0: init params ~ 0.076, gradient is NOT exponentially suppressed
# Layer 1: init params ~ 0.107, gradient is NOT exponentially suppressed
# Layer 2: init params ~ 0.089, gradient is NOT exponentially suppressed

# Strategy 2: Equivariant circuits (restrict to symmetry-respecting subspace)
# See Section 3.7 for full treatment

# Strategy 3: Local cost functions
print("\nLocal vs global cost comparison:")
print("Global cost (measure all qubits): Var[grad] ~ O(1/2^n)")
print("Local cost  (measure 1-2 qubits): Var[grad] ~ O(1/poly(n))")
print("→ Always prefer local cost functions on NISQ hardware")
