"""
Pre Quantum - Chapter 08: Quantum Information Essentials
Code Example: Beat 3: The Concept Build > 3.2 The No-Cloning Family: Approximate Cloning and No-Deleting
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-08/example_05_the_no_cloning_family_approximate_clonin.py
"""

import numpy as np

# The optimal universal 1→2 cloner achieves fidelity 5/6 for ANY input state.
# This is a fundamental limit, not an engineering limitation.

def optimal_clone_fidelity_qubit(N):
    """Optimal fidelity for 1→N universal cloning of qubits.

    Gisin-Massar (1997): F = (2N + 1) / (3N)
    N=2: 5/6 ≈ 0.8333 (Buzek-Hillery limit)
    N→∞: 2/3 (matches optimal measure-and-prepare strategy)
    """
    return (2 * N + 1) / (3 * N)

print("Optimal universal cloning fidelities (qubits):")
print(f"  1 → 2 copies:   F = {optimal_clone_fidelity_qubit(2):.6f}  (= 5/6)")
print(f"  1 → 3 copies:   F = {optimal_clone_fidelity_qubit(3):.6f}  (= 7/9)")
print(f"  1 → 10 copies:  F = {optimal_clone_fidelity_qubit(10):.6f}")
print(f"  1 → 100 copies: F = {optimal_clone_fidelity_qubit(100):.6f}")

# As N → ∞: F → 2/3, which equals the classical "measure and prepare" bound.
# This makes sense: with infinite copies, the cloner is effectively doing
# a measurement (extracting classical information) and then preparing copies.
print(f"  1 → ∞ copies:   F → {2/3:.6f}  (= 2/3)")
print(f"\n  Compare: random guess fidelity = {1/2:.4f}")
print(f"  The N→∞ limit (2/3) matches the optimal classical strategy:")
print(f"  measure the qubit optimally, then prepare N copies from the result.")
print(f"  Quantum cloning CAN beat classical for small N (5/6 > 2/3),")
print(f"  but the advantage vanishes as N → ∞.")

# State-dependent cloning can do better if you know the input is from a
# restricted set. For example, if the input is guaranteed to be |0⟩ or |1⟩
# (a known basis), you can clone perfectly -- that's just CNOT.
# The 5/6 limit is for UNIVERSAL cloning: works for ANY input state.

# Phase-covariant cloner: if input is on the equator of the Bloch sphere
# (all states of form cos(θ/2)|0⟩ + e^{iφ}sin(θ/2)|1⟩ with fixed θ=π/2),
# the optimal fidelity is (1 + 1/√2)/2 ≈ 0.8536 > 5/6.
phase_covariant_f = (1 + 1/np.sqrt(2)) / 2
print(f"\nPhase-covariant 1→2 fidelity: {phase_covariant_f:.6f}")
print(f"Universal 1→2 fidelity:       {optimal_clone_fidelity(2):.6f}")
print(f"More prior knowledge → higher fidelity clones")
