"""
Pre Quantum - Chapter 12: Shors Algorithm and QFT
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-12/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
import numpy as np
from math import gcd

# Shor's algorithm to factor N=15
# Step 1: Choose a random base (we pick a=7)
N = 15
a = 7

# Step 2: Build the quantum circuit for period finding
# We need to find r such that a^r ≡ 1 (mod N)
# For a=7, N=15: 7^1=7, 7^2=4, 7^3=13, 7^4=1 → r=4

# Use 3 counting qubits and 4 target qubits
n_count = 3  # precision qubits
n_target = 4  # enough to hold values mod 15

qc = QuantumCircuit(n_count + n_target, n_count)

# Superposition on counting register
qc.h(range(n_count))

# Initialize target to |1⟩ (for modular exponentiation: a^0 = 1)
qc.x(n_count)

# Controlled modular exponentiation: |j⟩|y⟩ → |j⟩|y · a^(2^j) mod N⟩
# For a=7, N=15, we hardcode the controlled operations:
# 7^1 mod 15 = 7:  controlled swap sequence
# 7^2 mod 15 = 4:  controlled swap sequence
# 7^4 mod 15 = 1:  identity (no-op)

# Controlled-7^1 mod 15 (controlled on qubit 0)
qc.cswap(0, n_count+0, n_count+1)
qc.cswap(0, n_count+1, n_count+2)
qc.cswap(0, n_count+2, n_count+3)

# Controlled-7^2 mod 15 = controlled-4 mod 15
qc.cswap(1, n_count+1, n_count+3)
qc.cswap(1, n_count+0, n_count+2)

# Controlled-7^4 mod 15 = identity (7^4 mod 15 = 1)
# No gates needed for qubit 2

# Inverse QFT on counting register
qc.swap(0, 2)
qc.h(0)
qc.cp(-np.pi/2, 1, 0)
qc.h(1)
qc.cp(-np.pi/4, 2, 0)
qc.cp(-np.pi/2, 2, 1)
qc.h(2)

# Measure counting register
qc.measure(range(n_count), range(n_count))

# Run with Qiskit 2.x StatevectorSampler
# (AerSimulator also works but StatevectorSampler is the modern primitive)
from qiskit_aer import AerSimulator
sim = AerSimulator()
result = sim.run(qc, shots=1024, seed_simulator=42).result()
counts = result.get_counts()

print(f"Factoring N={N} with a={a}")
print(f"Measurement results (counting register):")
for state, count in sorted(counts.items(), key=lambda x: -x[1]):
    phase = int(state, 2) / 2**n_count
    print(f"  |{state}⟩ ({count:4d}/1024)  →  phase = {phase:.4f}")

# Extract period from phases
print(f"\nPhases suggest period r=4")
print(f"Check: {a}^4 mod {N} = {pow(a, 4, N)}")

# Factor using the period
r = 4
factor1 = gcd(a**(r//2) - 1, N)
factor2 = gcd(a**(r//2) + 1, N)
print(f"\ngcd({a}^{r//2} - 1, {N}) = gcd({a**(r//2) - 1}, {N}) = {factor1}")
print(f"gcd({a}^{r//2} + 1, {N}) = gcd({a**(r//2) + 1}, {N}) = {factor2}")
print(f"\n{N} = {factor1} × {factor2}")
