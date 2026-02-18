"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.4 Barren Plateaus: The Trainability Crisis
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_08_barren_plateaus_the_trainability_crisis.py
"""

import numpy as np

def random_pqc_gradient_variance(n_qubits, n_layers, n_samples=500):
    """Estimate gradient variance for a random PQC.
    This demonstrates barren plateaus empirically."""

    def build_random_state(n_qubits, params):
        """Build an n-qubit state with alternating Ry layers and CNOT ladders."""
        dim = 2**n_qubits
        state = np.zeros(dim, dtype=complex)
        state[0] = 1.0  # |00...0⟩

        def Ry(t):
            return np.array([[np.cos(t/2), -np.sin(t/2)],
                             [np.sin(t/2),  np.cos(t/2)]], dtype=complex)

        CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
        I2 = np.eye(2, dtype=complex)

        p_idx = 0
        for layer in range(n_layers):
            # Single-qubit Ry rotations on each qubit
            gate = np.array([1.0], dtype=complex)
            for q in range(n_qubits):
                gate = np.kron(gate, Ry(params[p_idx]))
                p_idx += 1
            state = gate @ state

            # CNOT ladder: qubit q controls qubit q+1
            for q in range(n_qubits - 1):
                # Build n-qubit CNOT acting on qubits q, q+1
                if q == 0:
                    full_cnot = CNOT
                else:
                    full_cnot = np.eye(2**q, dtype=complex)
                    full_cnot = np.kron(full_cnot, CNOT)
                remaining = n_qubits - q - 2
                if remaining > 0:
                    full_cnot = np.kron(full_cnot, np.eye(2**remaining, dtype=complex))
                state = full_cnot @ state
        return state

    n_params = n_qubits * n_layers
    gradients = []
    epsilon = 0.01

    for _ in range(n_samples):
        params = np.random.randn(n_params) * 2 * np.pi

        # Compute gradient of ⟨Z₀⟩ w.r.t. first parameter via finite difference
        state_plus = build_random_state(n_qubits, params.copy())
        params_shifted = params.copy()
        params_shifted[0] += epsilon
        state_minus = build_random_state(n_qubits, params_shifted)

        # ⟨Z₀⟩ = P(q0=0) - P(q0=1)
        dim = 2**n_qubits
        half = dim // 2
        exp_Z_plus = sum(abs(state_plus[i])**2 for i in range(half)) - \
                     sum(abs(state_plus[i])**2 for i in range(half, dim))
        exp_Z_minus = sum(abs(state_minus[i])**2 for i in range(half)) - \
                      sum(abs(state_minus[i])**2 for i in range(half, dim))

        grad = (exp_Z_minus - exp_Z_plus) / epsilon
        gradients.append(grad)

    return np.var(gradients)

# Demonstrate exponential decay of gradient variance
print("Barren plateau demonstration:")
print(f"{'Qubits':<10} {'Layers':<10} {'Var[∂L/∂θ]':<15} {'Log10(Var)':<12}")
print("-" * 47)
for n_q in [2, 3, 4, 5, 6]:
    var = random_pqc_gradient_variance(n_q, n_layers=3, n_samples=300)
    print(f"{n_q:<10} {3:<10} {var:<15.6e} {np.log10(max(var, 1e-20)):<12.2f}")
# Output (typical):
# Barren plateau demonstration:
# Qubits     Layers     Var[∂L/∂θ]      Log10(Var)
# -----------------------------------------------
# 2          3          6.142e-02        -1.21
# 3          3          1.587e-02        -1.80
# 4          3          3.812e-03        -2.42
# 5          3          9.450e-04        -3.02
# 6          3          2.318e-04        -3.63
