"""
Pre Quantum - Chapter 13: Variational Algorithms
Code Example: Beat 3: The Concept Build > 3.6 ADAPT-VQE: Let the Algorithm Build the Ansatz
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-13/example_07_adapt_vqe_let_the_algorithm_build_the_an.py
"""

import numpy as np
from scipy.optimize import minimize

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Hamiltonian: H = -ZZ - 0.5(XI + IX) + 0.3 YY
H = (-np.kron(Z, Z) - 0.5 * (np.kron(X, I) + np.kron(I, X))
     + 0.3 * np.kron(Y, Y))

exact_E0 = np.linalg.eigvalsh(H)[0]
print(f"Exact ground state energy: {exact_E0:.6f}")

# Operator pool: generators that produce entangling unitaries e^{-iθA}
# For 2 qubits, a minimal pool includes:
operator_pool = {
    'YI': np.kron(Y, I),
    'IY': np.kron(I, Y),
    'XI': np.kron(X, I),
    'IX': np.kron(I, X),
    'XX-YY': np.kron(X, X) - np.kron(Y, Y),  # single excitation generator
    'XY+YX': np.kron(X, Y) + np.kron(Y, X),  # another excitation
}

def apply_unitary(state, generator, theta):
    """Apply e^{-iθA} to state using matrix exponential."""
    U = np.eye(4, dtype=complex) * np.cos(theta) - 1j * generator * np.sin(theta)
    # Only exact for A^2 = I (Pauli products). For general A, use expm.
    from scipy.linalg import expm
    U = expm(-1j * theta * generator)
    return U @ state

def energy(state):
    return np.real(state.conj() @ H @ state)

def gradient_of_operator(state, generator):
    """Compute |d⟨E⟩/dθ| at θ=0 for appending e^{-iθA} to current state.

    By the parameter shift rule: dE/dθ = -i⟨ψ|[H, A]|ψ⟩
    which simplifies to 2 * Im(⟨ψ|H A|ψ⟩).
    """
    commutator = H @ generator - generator @ H
    return abs(np.real(-1j * state.conj() @ commutator @ state))

# ADAPT-VQE loop
state = np.array([1, 0, 0, 0], dtype=complex)  # |00⟩
selected_ops = []   # (name, generator) pairs
all_params = []     # accumulated parameters

print(f"\nADAPT-VQE iteration log:")
print(f"{'Step':>4} {'Selected':>10} {'Gradient':>10} {'Energy':>12} {'Error':>12}")

for step in range(6):
    # 1. Compute gradient for each operator in the pool
    grads = {}
    for name, gen in operator_pool.items():
        grads[name] = gradient_of_operator(state, gen)

    # 2. Pick the operator with largest gradient
    best_op = max(grads, key=grads.get)
    best_grad = grads[best_op]

    # Convergence check: if all gradients are tiny, stop
    if best_grad < 1e-6:
        print(f"  Converged at step {step}: all gradients < 1e-6")
        break

    selected_ops.append((best_op, operator_pool[best_op]))
    all_params.append(0.0)  # initialize new parameter

    # 3. Re-optimize ALL parameters jointly
    def adapt_cost(params):
        s = np.array([1, 0, 0, 0], dtype=complex)
        for i, (_, gen) in enumerate(selected_ops):
            s = apply_unitary(s, gen, params[i])
        return energy(s)

    result = minimize(adapt_cost, x0=all_params, method='COBYLA',
                      options={'maxiter': 200})
    all_params = list(result.x)

    # Rebuild the state with optimized params
    state = np.array([1, 0, 0, 0], dtype=complex)
    for i, (_, gen) in enumerate(selected_ops):
        state = apply_unitary(state, gen, all_params[i])

    err = abs(energy(state) - exact_E0)
    print(f"{step:4d} {best_op:>10} {best_grad:10.6f} {energy(state):12.6f} {err:12.8f}")

print(f"\nFinal ADAPT-VQE energy: {energy(state):.6f}")
print(f"Operators used: {[name for name, _ in selected_ops]}")
print(f"Parameters: {len(all_params)} (vs 6 for fixed ansatz)")
