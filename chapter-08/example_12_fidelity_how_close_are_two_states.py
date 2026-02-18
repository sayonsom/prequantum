"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.5 Fidelity: How Close Are Two States?
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_12_fidelity_how_close_are_two_states.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity
from scipy.linalg import sqrtm

# Qiskit's state_fidelity handles both pure and mixed states
sv_0 = Statevector.from_label('0')
sv_1 = Statevector.from_label('1')
sv_plus = Statevector.from_label('+')

print("Pure-state fidelity (via Qiskit):")
print(f"  F(|0⟩, |0⟩) = {state_fidelity(sv_0, sv_0):.4f}")  # 1.0
print(f"  F(|0⟩, |1⟩) = {state_fidelity(sv_0, sv_1):.4f}")  # 0.0
print(f"  F(|0⟩, |+⟩) = {state_fidelity(sv_0, sv_plus):.4f}")  # 0.5

# Mixed-state fidelity: compare a pure state to a noisy (mixed) version
# The maximally mixed state ρ = I/2 (completely random qubit)
rho_mixed = DensityMatrix(np.eye(2) / 2)
rho_pure_0 = DensityMatrix(sv_0)

print(f"\nMixed-state fidelity:")
print(f"  F(|0⟩, I/2) = {state_fidelity(rho_pure_0, rho_mixed):.4f}")  # 0.5

# A depolarized state: ρ = (1-p)|0⟩⟨0| + p·I/2
for p in [0.0, 0.01, 0.05, 0.10, 0.50, 1.00]:
    rho_depol = (1 - p) * rho_pure_0.data + p * np.eye(2) / 2
    rho_depol = DensityMatrix(rho_depol)
    f = state_fidelity(rho_pure_0, rho_depol)
    print(f"  F(|0⟩, depolarized p={p:.2f}) = {f:.4f}")

# Fidelity after a noisy circuit
ideal_circuit = QuantumCircuit(1)
ideal_circuit.h(0)
ideal_state = Statevector.from_instruction(ideal_circuit)

noisy_circuit = QuantumCircuit(1)
noisy_circuit.h(0)
noisy_circuit.rz(0.05, 0)  # Tiny unwanted phase rotation (simulating error)
noisy_state = Statevector.from_instruction(noisy_circuit)

f = state_fidelity(ideal_state, noisy_state)
print(f"\nFidelity after small phase error: {f:.6f}")
print(f"Infidelity (1-F): {1-f:.6f}")
