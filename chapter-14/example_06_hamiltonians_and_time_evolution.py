"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.2 Hamiltonians and Time Evolution
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_06_hamiltonians_and_time_evolution.py
"""

import numpy as np
from scipy.linalg import expm

# Hamiltonian: X gate
X = np.array([[0, 1], [1, 0]], dtype=complex)
eigenvalues, eigenvectors = np.linalg.eigh(X)

def fast_time_evolution(eigenvalues, eigenvectors, t):
    """Compute e^{-iHt} using eigendecomposition -- O(n²) per time step."""
    phases = np.exp(-1j * eigenvalues * t)
    # U(t) = Σ_i e^{-iλ_i t} |v_i⟩⟨v_i|
    U = sum(phases[i] * np.outer(eigenvectors[:, i], eigenvectors[:, i].conj())
            for i in range(len(eigenvalues)))
    return U

# Compare with scipy expm
t = 0.75
U_eigen = fast_time_evolution(eigenvalues, eigenvectors, t)
U_expm = expm(-1j * X * t)
print(f"Eigendecomp matches expm: {np.allclose(U_eigen, U_expm)}")

# Benchmark: many time steps
import time
n_steps = 1000
times = np.linspace(0, 2*np.pi, n_steps)

start = time.perf_counter()
for t in times:
    _ = fast_time_evolution(eigenvalues, eigenvectors, t)
eigen_time = time.perf_counter() - start

start = time.perf_counter()
for t in times:
    _ = expm(-1j * X * t)
expm_time = time.perf_counter() - start

print(f"Eigendecomp: {eigen_time:.3f}s for {n_steps} steps")
print(f"expm:        {expm_time:.3f}s for {n_steps} steps")
print(f"Speedup:     {expm_time/eigen_time:.1f}x")
